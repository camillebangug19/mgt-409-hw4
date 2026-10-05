from pathlib import Path
import sqlite3

try:
    from .audit import audited_tool_call
    from .models import ProductCard, ProductDetails, StockOption
except ImportError:
    from audit import audited_tool_call
    from models import ProductCard, ProductDetails, StockOption


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "campus_customs.db"


def _connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _stock_options(connection: sqlite3.Connection, product_id: str) -> list[StockOption]:
    inventory = connection.execute(
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
    return [StockOption(**dict(item)) for item in inventory]


def _product_card(row: sqlite3.Row, sizes: list[StockOption]) -> ProductCard:
    return ProductCard(
        product_id=row["product_id"],
        name=row["name"],
        price=row["price"],
        description=row["description"],
        image_url=f"/images/{row['image_file_path']}",
        sizes=sizes,
    )


def search_products(query: str) -> list[ProductCard]:
    """Search the Campus Customs catalogue and return matching products with stock by size."""
    return audited_tool_call("search_products", {"query": query}, lambda: _search_products(query))


def _search_products(query: str) -> list[ProductCard]:
    tokens = [token.lower() for token in query.split() if token.strip()]
    if not tokens:
        return []

    clauses: list[str] = []
    parameters: list[str] = []
    searchable_fields = ("name", "garment_type", "description", "colors", "search_tags")
    for token in tokens:
        variants = [token]
        if token.endswith("ies"):
            variants.extend([f"{token[:-3]}y", f"{token[:-3]}ie"])
        elif token.endswith("s") and len(token) > 3:
            variants.append(token[:-1])
        clauses.append("(" + " OR ".join(f"LOWER({field}) LIKE ?" for field in searchable_fields for _ in variants) + ")")
        parameters.extend([f"%{variant}%" for field in searchable_fields for variant in variants])

    with _connection() as connection:
        rows = connection.execute(
            f"""
            SELECT product_id, name, description, image_file_path, price
            FROM catalogue
            WHERE {' AND '.join(clauses)}
            ORDER BY name
            LIMIT 6
            """,
            parameters,
        ).fetchall()

        cards: list[ProductCard] = []
        for row in rows:
            cards.append(_product_card(row, _stock_options(connection, row["product_id"])))
    return cards


def get_product_details(product_id: str) -> ProductDetails | None:
    """Look up one catalogue product by ID with its exact description, price, and stock by size."""
    return audited_tool_call(
        "get_product_details",
        {"product_id": product_id},
        lambda: _get_product_details(product_id),
    )


def _get_product_details(product_id: str) -> ProductDetails | None:
    with _connection() as connection:
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
            return None
        return ProductDetails(
            product_id=row["product_id"],
            name=row["name"],
            garment_type=row["garment_type"],
            description=row["description"],
            colors=row["colors"],
            search_tags=row["search_tags"],
            price=row["price"],
            image_url=f"/images/{row['image_file_path']}",
            sizes=_stock_options(connection, row["product_id"]),
        )
