from pathlib import Path
import hashlib
import hmac
import json
import re
import secrets
import sqlite3
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

try:
    from .audit import audit_run, finish_agent_run, start_agent_run
    from .agent import shop_agent
    from .models import ChatHistoryMessage, ChatReply, ChatRequest, ShopperDeps, WoofRequest, WoofResponse
    from .tools import get_product_details
except ImportError:
    from audit import audit_run, finish_agent_run, start_agent_run
    from agent import shop_agent
    from models import ChatHistoryMessage, ChatReply, ChatRequest, ShopperDeps, WoofRequest, WoofResponse
    from tools import get_product_details


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "campus_customs.db"
DATA_PATH = PROJECT_ROOT / "data"
PASSWORD_ITERATIONS = 120_000
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
AMBIGUOUS_PRODUCT_REFERENCE_PATTERN = re.compile(r"\b(this|that|that one|the other one|it)\b", re.IGNORECASE)

app = FastAPI(title="Campus Customs API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Catalogue image_file_path values are relative to data/, e.g. products/foo.jpg.
app.mount("/images", StaticFiles(directory=DATA_PATH), name="images")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def ensure_application_tables() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS saved_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES catalogue(product_id),
                UNIQUE (user_id, product_id)
            )
            """
        )


ensure_application_tables()


def product_from_row(row: sqlite3.Row) -> dict[str, Any]:
    product = dict(row)
    product["image_url"] = f"/images/{product.pop('image_file_path')}"
    product["category"] = product_category(product["garment_type"])["slug"]
    return product


CATEGORY_RULES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("short-sleeves", "Short Sleeves", ("short-sleeve", "t-shirt")),
    ("long-sleeves", "Long Sleeves", ("long-sleeve",)),
    ("sweatshirts-hoodies", "Sweatshirts & Hoodies", ("sweatshirt", "hoodie", "crewneck", "mockneck", "quarter-zip", "pullover")),
    ("jackets-outerwear", "Jackets & Outerwear", ("jacket",)),
)


def product_category(garment_type: str) -> dict[str, str]:
    normalized_type = garment_type.casefold()
    for slug, label, terms in CATEGORY_RULES:
        if any(term in normalized_type for term in terms):
            return {"slug": slug, "name": label}
    return {"slug": "other-apparel", "name": "Other Apparel"}


class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


def normalize_email(email: str) -> str:
    normalized = email.strip().lower()
    if not EMAIL_PATTERN.fullmatch(normalized):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    return normalized


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    ).hex()
    return f"pbkdf2_sha256${salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, salt, expected_digest = stored_hash.split("$", 2)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    candidate_digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    ).hex()
    return hmac.compare_digest(candidate_digest, expected_digest)


def public_user(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, __: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "Please check the request fields and try again."},
    )


@app.exception_handler(sqlite3.Error)
async def database_exception_handler(_: Request, __: sqlite3.Error) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": "Campus Customs data is temporarily unavailable. Please try again shortly."},
    )


def resolve_chat_user(user_id: int | None, user_email: str | None) -> sqlite3.Row | None:
    if user_id is None and user_email is None:
        return None
    if user_id is None or user_email is None:
        raise HTTPException(status_code=401, detail="Log in to save chat history.")
    email = normalize_email(user_email)
    with get_connection() as connection:
        user = connection.execute(
            "SELECT id, name, email, first_name, last_name FROM users WHERE id = ? AND email = ?",
            (user_id, email),
        ).fetchone()
    if user is None:
        raise HTTPException(status_code=401, detail="Log in to save chat history.")
    return user


def page_context_text(page_context: Any) -> str | None:
    if page_context is None:
        return None
    if page_context.product_id:
        product = get_product_details(page_context.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="That product page could not be found.")
        return (
            f"The shopper is viewing the product detail page for {product.name} "
            f"(product_id: {product.product_id}). Exact description: {product.description} "
            f"Exact price: ${product.price:.2f}. Colors: {product.colors}."
        )
    return f"The shopper is on page {page_context.path}."


def ambiguous_product_clarification(request: ChatRequest) -> ChatReply | None:
    if request.page_context is not None and request.page_context.product_id:
        return None
    if not AMBIGUOUS_PRODUCT_REFERENCE_PATTERN.search(request.message):
        return None

    products = []
    seen_ids: set[str] = set()
    for turn in reversed(request.conversation):
        for product in turn.products:
            if product.product_id not in seen_ids:
                products.append(product)
                seen_ids.add(product.product_id)
    if len(products) < 2:
        return None

    names = ", ".join(product.name for product in products[:4])
    return ChatReply(
        reply=f"Which product do you mean—{names}? Tell me which one and I’ll check its exact catalogue details.",
        products=[],
    )


def save_chat_exchange(user: sqlite3.Row, message: str, reply: ChatReply) -> None:
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO chat_messages (user_id, role, content) VALUES (?, 'user', ?)",
            (user["id"], message),
        )
        connection.execute(
            "INSERT INTO chat_messages (user_id, role, content, products_json) VALUES (?, 'assistant', ?, ?)",
            (user["id"], reply.reply, json.dumps([product.model_dump() for product in reply.products])),
        )


@app.post("/chat", response_model=ChatReply)
async def chat(request: ChatRequest) -> ChatReply:
    user = resolve_chat_user(request.user_id, request.user_email)
    clarification = ambiguous_product_clarification(request)
    if clarification is not None:
        if user is not None:
            save_chat_exchange(user, request.message, clarification)
        return clarification

    deps = ShopperDeps(
        user_id=user["id"] if user else None,
        name=user["name"] if user else None,
        email=user["email"] if user else None,
        page_context=page_context_text(request.page_context),
        conversation=request.conversation,
    )
    audit_run_id = start_agent_run(request.message)
    try:
        with audit_run(audit_run_id):
            result = await shop_agent.run(request.message, deps=deps)
    except Exception as error:
        finish_agent_run(audit_run_id, stop_reason="error", result={"error": str(error)})
        print(f"Chat agent error: {error}")
        return ChatReply(
            reply="I’m sorry—I’m having trouble reaching the Campus Customs catalogue right now. I don’t want to guess, so please try your question again in a moment.",
            products=[],
        )
    finish_reason = getattr(result.response, "finish_reason", None) or "completed"
    if hasattr(finish_reason, "value"):
        finish_reason = finish_reason.value
    finish_agent_run(audit_run_id, stop_reason=str(finish_reason), result=result.output)
    reply = result.output
    if user is not None:
        save_chat_exchange(user, request.message, reply)
    return reply


@app.get("/api/chat/history/{user_id}", response_model=list[ChatHistoryMessage])
def chat_history(user_id: int, email: str = Query(min_length=3, max_length=254)) -> list[ChatHistoryMessage]:
    user = resolve_chat_user(user_id, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Log in to load chat history.")
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, role, content, products_json, created_at
            FROM chat_messages
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,),
        ).fetchall()
    history: list[ChatHistoryMessage] = []
    for row in rows:
        products = json.loads(row["products_json"]) if row["products_json"] else []
        history.append(ChatHistoryMessage(id=row["id"], role=row["role"], content=row["content"], products=products, created_at=row["created_at"]))
    return history


@app.get("/api/woofs/{user_id}", response_model=list[WoofResponse])
def list_woofs(user_id: int, email: str = Query(min_length=3, max_length=254)) -> list[WoofResponse]:
    user = resolve_chat_user(user_id, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Log in to view Your Woofs.")

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT product_id
            FROM saved_products
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (user_id,),
        ).fetchall()

    saved: list[WoofResponse] = []
    for row in rows:
        product = get_product_details(row["product_id"])
        if product is not None:
            saved.append(WoofResponse(saved=True, product=product))
    return saved


@app.post("/api/woofs", response_model=WoofResponse)
def toggle_woof(request: WoofRequest) -> WoofResponse:
    user = resolve_chat_user(request.user_id, request.user_email)
    if user is None:
        raise HTTPException(status_code=401, detail="Log in to save a product.")

    product = get_product_details(request.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="That product could not be found.")

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM saved_products WHERE user_id = ? AND product_id = ?",
            (request.user_id, request.product_id),
        ).fetchone()
        if existing is None:
            connection.execute(
                "INSERT INTO saved_products (user_id, product_id) VALUES (?, ?)",
                (request.user_id, request.product_id),
            )
            saved = True
        else:
            connection.execute("DELETE FROM saved_products WHERE id = ?", (existing["id"],))
            saved = False
    return WoofResponse(saved=saved, product=product)


@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest) -> dict[str, Any]:
    email = normalize_email(request.email)
    first_name = request.first_name.strip()
    last_name = request.last_name.strip()
    if not first_name or not last_name:
        raise HTTPException(status_code=422, detail="First and last name are required.")

    with get_connection() as connection:
        existing_user = connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        if existing_user is not None:
            raise HTTPException(status_code=409, detail="An account with that email already exists.")

        cursor = connection.execute(
            """
            INSERT INTO users (name, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
            """,
            (f"{first_name} {last_name}", email, hash_password(request.password), first_name, last_name),
        )
        user = connection.execute(
            "SELECT id, name, email, first_name, last_name FROM users WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return {"message": "Your Campus Customs account has been created.", "user": public_user(user)}


@app.post("/api/auth/login")
def login(request: LoginRequest) -> dict[str, Any]:
    email = normalize_email(request.email)
    with get_connection() as connection:
        user = connection.execute(
            "SELECT id, name, email, password_hash, first_name, last_name FROM users WHERE email = ?",
            (email,),
        ).fetchone()

    if user is None or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")

    return {"message": "You’re signed in.", "user": public_user(user)}


@app.get("/api/products")
def list_products() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT product_id, name, garment_type, description, colors,
                   search_tags, image_file_path, price
            FROM catalogue
            ORDER BY name
            """
        ).fetchall()
    return [product_from_row(row) for row in rows]


@app.get("/api/product-categories")
def list_product_categories() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT garment_type, COUNT(*) AS count
            FROM catalogue
            GROUP BY garment_type
            ORDER BY garment_type COLLATE NOCASE
            """
        ).fetchall()

    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        category = product_category(row["garment_type"])
        grouped.setdefault(
            category["slug"],
            {"slug": category["slug"], "name": category["name"], "count": 0},
        )["count"] += row["count"]
    return sorted(grouped.values(), key=lambda category: category["name"])


@app.get("/api/products/{product_id}")
def get_product(product_id: str) -> dict[str, Any]:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT product_id, name, garment_type, description, colors,
                   search_tags, image_file_path, price
            FROM catalogue
            WHERE product_id = ?
            """,
            (product_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")

        inventory_rows = connection.execute(
            """
            SELECT size, quantity
            FROM inventory
            WHERE product_id = ?
            ORDER BY CASE size
                WHEN 'XS' THEN 1
                WHEN 'S' THEN 2
                WHEN 'M' THEN 3
                WHEN 'L' THEN 4
                WHEN 'XL' THEN 5
                WHEN 'XXL' THEN 6
                ELSE 7
            END
            """,
            (product_id,),
        ).fetchall()

    product = product_from_row(row)
    product["sizes"] = [dict(inventory_row) for inventory_row in inventory_rows]
    return product
