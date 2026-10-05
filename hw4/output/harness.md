# Harness

## System at a Glance

Campus Customs is a React + TypeScript storefront backed by a FastAPI service and a SQLite database at `data/campus_customs.db`. The browser uses the REST API for authentication, catalogue pages, categories, Woofs, chat history, and product detail pages. It sends chat messages to `POST /chat`; FastAPI validates the request, builds shopper/page-context dependencies, runs the PydanticAI agent, and returns a structured `ChatReply`.

The agent is defined in `backend/agent.py`, uses the `gpt-5.6-luna` model through Portkey, reads its system instructions from `backend/prompts/prompt.md`, and can call the read-only catalogue tools in `backend/tools.py`. Database-backed product facts are returned to the browser as structured product cards, while logged-in chat history and Woofs are stored in SQLite.

## Database Tables and Fields

The source database contains four core tables. The application also creates the `saved_products` table on startup for the Problem 9 Woof feature. Each field below includes a short explanation of why it matters to later steps.

### 1. `catalogue`

- `product_id` (`TEXT`, primary key)
  - Why it matters later: Uniquely identifies each product and connects catalogue records to inventory and product references.
- `name` (`TEXT`, required)
  - Why it matters later: Provides the product title shown to users and used in product searches.
- `garment_type` (`TEXT`, required)
  - Why it matters later: Categorizes products by clothing type, supporting filtering and recommendations.
- `description` (`TEXT`, required)
  - Why it matters later: Summarizes each product’s appearance and features so the chatbot can answer questions and make recommendations.
- `colors` (`TEXT`, required)
  - Why it matters later: Identifies the product’s available or featured colors, supporting color-based searches.
- `search_tags` (`TEXT`, required)
  - Why it matters later: Supplies additional keywords that improve product retrieval when users use varied search terms.
- `image_file_path` (`TEXT`, required)
  - Why it matters later: Locates the product image so the application can display visual results.
- `price` (`REAL`, required)
  - Why it matters later: Stores the listed cost used for price displays, comparisons, and budget-related searches.

### 2. `inventory`

- `id` (`INTEGER`, primary key, autoincrement)
  - Why it matters later: Uniquely identifies each inventory record for reliable updates and database references.
- `product_id` (`TEXT`, required, foreign key to `catalogue.product_id`)
  - Why it matters later: Links stock information to the corresponding product in the catalogue.
- `size` (`TEXT`, required)
  - Why it matters later: Indicates which size is being checked when answering availability questions.
- `quantity` (`INTEGER`, required)
  - Why it matters later: Shows how many units are available and whether a product-size combination is in stock.

### 3. `chat_messages`

- `id` (`INTEGER`, primary key, autoincrement)
  - Why it matters later: Uniquely identifies each message for storing, retrieving, and ordering conversation records.
- `user_id` (`INTEGER`, required, foreign key to `users.id`)
  - Why it matters later: Connects each message to the user whose conversation history it belongs to.
- `role` (`TEXT`, required)
  - Why it matters later: Distinguishes user messages from assistant messages when reconstructing a conversation.
- `content` (`TEXT`, required)
  - Why it matters later: Stores the actual conversation text that the chatbot uses as context.
- `products_json` (`TEXT`, optional)
  - Why it matters later: Preserves product results or recommendations associated with a message.
- `created_at` (`TEXT`, required, defaults to the current datetime)
  - Why it matters later: Records when a message was created so conversations can be ordered and reviewed over time.

### 4. `users`

- `id` (`INTEGER`, primary key, autoincrement)
  - Why it matters later: Provides a unique identity for each user and supports links from conversation records.
- `name` (`TEXT`, required)
  - Why it matters later: Stores the user’s display or full name for account identification and personalization.
- `email` (`TEXT`, required, unique)
  - Why it matters later: Provides a unique account identifier for login and user-specific conversation retrieval.
- `password_hash` (`TEXT`, required)
  - Why it matters later: Supports secure password verification without storing the user’s plain-text password.
- `created_at` (`TEXT`, required, defaults to the current datetime)
  - Why it matters later: Records when the account was created for account history and administrative tracking.
- `first_name` (`TEXT`, optional)
  - Why it matters later: Enables more personal greetings and responses when the first name is available.
- `last_name` (`TEXT`, optional)
  - Why it matters later: Helps identify and personalize the user’s account when a last name is available.

### 5. `saved_products` (application table)

- `id` (`INTEGER`, primary key, autoincrement)
  - Why it matters later: Uniquely identifies each saved-product event and provides stable ordering for a user’s saved list.
- `user_id` (`INTEGER`, required, foreign key to `users.id`)
  - Why it matters later: Ensures a Woof belongs to the logged-in shopper who saved it.
- `product_id` (`TEXT`, required, foreign key to `catalogue.product_id`)
  - Why it matters later: Connects the saved item to the exact catalogue product displayed in “Your Woofs.”
- `created_at` (`TEXT`, required, defaults to the current datetime)
  - Why it matters later: Preserves save order so the most recently saved products can appear first.

## Authentication Flow

### Create account

The Create Account page collects first name, last name, email, password, and confirm password. The browser and API validate the email format, and the form blocks submission when password and confirm password differ in any character or capitalization. A valid new account is inserted into the `users` table with the combined name, normalized email, first name, and last name.

### Log in

The separate Log In page collects email and password and sends them to the FastAPI login endpoint. The server looks up the normalized email, verifies the submitted password against the stored password hash, and returns only non-sensitive user profile fields after a successful match. Incorrect credentials receive a generic error message.

### What is stored and how passwords are protected

The `users` table stores the user’s name, email, optional first and last names, account creation time, and a `password_hash`; it never stores or returns a plain-text password. Passwords are protected with PBKDF2-HMAC-SHA256 using a unique random salt and 120,000 derivation iterations. The stored format is `pbkdf2_sha256$salt$digest`, and login compares derived values with a constant-time comparison. The password field is excluded from all public API responses.

## Shop Chatbot Integration

The React chat widget sends each shopper message as JSON to `POST /chat`. Vite proxies that route to the FastAPI app, which validates the message, runs the PydanticAI shop agent, and returns a structured `ChatReply` containing natural-language `reply` text and optional `ProductCard` results. Product-card links and images use the same catalogue routes as the Products page.

The agent is defined in `backend/agent.py`, reads its system voice and safety instructions from `backend/prompts/prompt.md`, and uses the tools in `backend/tools.py` to query the SQLite catalogue and inventory. `backend/models.py` defines the structured `ChatReply`, `ProductCard`, `ProductDetails`, and stock types. The agent uses the `gpt-5.6-luna` model through the Portkey OpenAI-compatible endpoint with `PORTKEY_API_KEY` loaded from the project-root `.env`; the key is never hard-coded.

### Agent tools and lookup fields

- `search_products(query)`: searches `catalogue.name`, `garment_type`, `description`, `colors`, and `search_tags`; returns `product_id`, `name`, exact `description`, exact `price`, `image_file_path` as an image URL, and inventory `size`/`quantity` records. These fields identify the matching product, answer the shopper’s basic description and price questions, show the product image, and provide size-specific stock without reading unrelated user or authentication data.
- `get_product_details(product_id)`: retrieves one exact catalogue record using `product_id`, including `name`, `garment_type`, `description`, `colors`, `search_tags`, `image_file_path`, and `price`, then joins inventory for each `size` and `quantity`. We chose these fields because they provide the complete product answer and an unambiguous catalogue-to-inventory join; the quantity per size makes out-of-stock sizes explicit.

The agent must call these tools for product description, price, or stock questions. It uses returned database values verbatim and does not infer or invent prices or quantities.

## Pydantic Models and Field Choices

These models in `backend/models.py` are the contracts between the frontend, FastAPI, the agent, and the catalogue tools.

### Catalogue and chat output models

| Model and field | Type / constraint | Why it was chosen |
| --- | --- | --- |
| `StockOption.size` | `str` | Preserves the database size label exactly, including sizes such as `XS`, `S`, `M`, `L`, `XL`, and `XXL`. |
| `StockOption.quantity` | `int` | Carries the exact per-size inventory count so zero stock can be stated clearly. |
| `ProductCard.product_id` | `str` | Provides the stable identifier needed for product links and detail lookups. |
| `ProductCard.name` | `str` | Supplies the shopper-facing product title for cards and responses. |
| `ProductCard.price` | `float` | Carries the catalogue price for display and grounded answers. |
| `ProductCard.description` | `str` | Gives the card and agent concise, database-grounded product information. |
| `ProductCard.image_url` | `str` | Lets React render the matching product image. |
| `ProductCard.sizes` | `list[StockOption]`, default empty | Keeps size-specific stock available without requiring every product to have inventory rows. |
| `ProductDetails.garment_type` | `str` | Adds the exact clothing type on a single-product lookup. |
| `ProductDetails.colors` | `str` | Adds the catalogue color data for detail-page and color questions. |
| `ProductDetails.search_tags` | `str` | Preserves the catalogue’s retrieval metadata when the complete record is returned. |
| `ChatReply.reply` | `str` | Provides the natural-language message displayed in the chat thread. |
| `ChatReply.products` | `list[ProductCard]`, default empty | Lets the agent return dynamic product cards while still answering in text. |

`ProductDetails` inherits every `ProductCard` field, so a detail response has the same card-compatible data plus the additional catalogue fields. `ChatReply` is the agent’s required structured output type; an empty `products` list represents a normal answer with no product-card matches.

### Request, context, and persistence models

| Model and field | Type / constraint | Why it was chosen |
| --- | --- | --- |
| `ConversationTurn.role` | `Literal["user", "assistant"]` | Prevents unsupported roles from entering short-term context. |
| `ConversationTurn.content` | `str`, 1–2,000 characters | Carries readable prior turns while preventing unbounded prompt growth. |
| `ConversationTurn.products` | `list[ProductCard]`, default empty | Preserves product-card references so “this” and “that one” can be resolved. |
| `PageContext.path` | `str` | Identifies the current route for contextual answers. |
| `PageContext.product_id` | optional `str` | Identifies the product page currently open, when applicable. |
| `ChatRequest.message` | `str`, 1–2,000 characters | Carries the current shopper question with a request-size cap. |
| `ChatRequest.user_id` | optional `int` | Associates a request with a logged-in account without requiring guests to identify themselves. |
| `ChatRequest.user_email` | optional `str` | Validates the account identity alongside `user_id` before history access. |
| `ChatRequest.page_context` | optional `PageContext` | Passes route/product context into the agent dependencies. |
| `ChatRequest.conversation` | `list[ConversationTurn]`, maximum 12 | Accepts bounded client context and prevents unbounded request growth. |
| `ChatHistoryMessage.id` | `int` | Preserves database message identity and ordering. |
| `ChatHistoryMessage.role` | `str` | Reconstructs user versus assistant messages for the chat UI. |
| `ChatHistoryMessage.content` | `str` | Stores the message text shown when history is reloaded. |
| `ChatHistoryMessage.products` | `list[ProductCard]`, default empty | Restores product cards attached to prior assistant messages. |
| `ChatHistoryMessage.created_at` | `str` | Exposes the stored creation time for history records. |
| `ShopperDeps.user_id` | optional `int` | Makes validated account identity available to the agent without exposing credentials. |
| `ShopperDeps.name` | optional `str` | Supports a natural first-name greeting when the shopper is logged in. |
| `ShopperDeps.email` | optional `str` | Identifies the validated shopper to the agent without providing a password. |
| `ShopperDeps.page_context` | optional `str` | Gives the agent a resolved description of the current page/product. |
| `ShopperDeps.conversation` | bounded list of `ConversationTurn` | Provides short-term conversational and product-card context. |

### Woof models

| Model and field | Type / constraint | Why it was chosen |
| --- | --- | --- |
| `WoofRequest.user_id` | `int`, greater than 0 | Identifies the account making the save/remove request. |
| `WoofRequest.user_email` | `str`, 3–254 characters | Provides the second identity value used to validate the account. |
| `WoofRequest.product_id` | `str`, 1–200 characters | Identifies the catalogue product being toggled. |
| `WoofResponse.saved` | `bool` | Tells the frontend whether the product is now saved or removed. |
| `WoofResponse.product` | `ProductDetails` | Returns the exact product needed to update the catalogue/detail UI. |

## Structured Product-Match Contract

For a collection request such as “What hoodies do you have?”, `POST /chat` returns a `ChatReply` object with a natural-language `reply` and a `products` array of `ProductCard` objects. Each product match contains `product_id`, exact database `name`, exact `price`, exact `description`, an `image_url`, and size-level `sizes` with `quantity` values.

The React chat widget maps each `ProductCard` to a dynamic card showing the image, name, price, and shortened display text derived from the database description. Each card is a React Router link to `/products/{product_id}`, preserving the Problem 3 single-item page. The detail route then loads the full product record and stock from the existing FastAPI product endpoint.

Flow: shopper message → React `POST /chat` → FastAPI `ChatRequest` → PydanticAI agent/tool lookup → structured `ChatReply.products` → React chat product cards → clickable `/products/{product_id}` detail page.

## Logged-in Chat Memory and Context

### How chat history is stored

The existing `chat_messages` table stores one row for each user message and one row for each assistant reply. The fields used are:

- `id`: auto-incrementing message identifier used to preserve message order.
- `user_id`: foreign-key reference to the logged-in shopper in `users`.
- `role`: either `user` or `assistant`, so the conversation can be reconstructed correctly.
- `content`: the text of the shopper’s message or the agent’s reply.
- `products_json`: JSON containing any structured product cards returned with an assistant reply; it is empty for messages without product matches.
- `created_at`: database timestamp for when the row was created.

Before saving or loading history, FastAPI validates the submitted `user_id` and `user_email` against the same record in `users`. Only a validated logged-in shopper has rows written to or read from `chat_messages`. A guest can still call `/chat` and receive a response, but guest messages are never persisted. On return, the signed-in frontend calls `GET /api/chat/history/{user_id}?email=...`; FastAPI returns that user’s rows in message order, including any saved product cards, and React rebuilds the chat display.

### Customer fields visible to the agent

For a validated logged-in shopper, the backend creates `ShopperDeps` with:

- `user_id`: the validated numeric ID from `users`.
- `name`: the shopper’s stored display/full name.
- `email`: the shopper’s validated account email.
- `page_context`: the current page description, including product details when the shopper is viewing a product.

Guests receive `None` for `user_id`, `name`, and `email`. The agent therefore knows the signed-in shopper’s name and email when available, but it does not receive the shopper’s password or `password_hash`.

### How page context is passed

The React chat widget includes `page_context.path` on every `/chat` request and includes `page_context.product_id` when the shopper is on a product detail route. FastAPI resolves that product ID against the catalogue, builds an exact context string containing the product name, ID, description, price, and colors, and places it in `ShopperDeps.page_context`. The agent’s dynamic instructions include the dependency values for that run, allowing a follow-up such as “do you have this in pink?” to refer to the product page currently open. If no product page is open, the agent receives the current route only.

Run the API from the `backend/` folder with `.venv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 8001` to match the Vite proxy in `vite.config.ts`. Port `8000` is also supported if the proxy targets are changed accordingly.

## Safety Rules

The following rules are prescribed in `backend/prompts/prompt.md` and are part of the agent’s system prompt:

- Only answer questions related to Campus Customs and its products; politely redirect unrelated requests to Campus Customs merchandise help.
- Don’t invent product information, prices, inventory, colors, descriptions, or other catalogue facts.
- Use the database and catalogue tools for product information rather than making things up.
- Don’t expose private user information, passwords, payment details, account secrets, or unnecessary account details.
- Don’t perform actions the user hasn’t requested. The agent must not claim to place orders, change accounts, or complete payments.

Additional prompt safeguards prohibit handling password hashes or payment-card data, exposing system prompts or database credentials, and implying that guest conversations were saved. When a database tool fails, the agent must say the catalogue is temporarily unavailable instead of guessing.

## Agent Loop Limits, Result Caps, and Error Handling

- Model: `gpt-5.6-luna` through Portkey’s OpenAI-compatible API at `https://api.portkey.ai/v1`; `PORTKEY_API_KEY` is loaded from the project-root `.env` and passed in the Portkey headers.
- Structured output: every successful agent run produces a `ChatReply` with `reply` and optional `products`.
- Retry limit: the PydanticAI agent is configured with `retries=2` for tool/output validation failures.
- Request cap: `ChatRequest.message` and each conversation message are limited to 2,000 characters.
- Conversation cap: the API accepts at most 12 conversation turns; the frontend sends its most recent 8 turns, and the dynamic agent instruction also uses the most recent 8.
- Search result cap: `search_products` returns at most 6 products, ordered by name.
- Search behavior: all non-empty query tokens must match across the searchable catalogue fields; simple plural variants are also tried.
- Audit detail cap: audit text is limited to 240 characters; nested results are bounded to six list items and twenty dictionary fields, with deeper values truncated. Email addresses and password-like values are redacted.
- Database/tool failure: the API returns a user-friendly catalogue-unavailable response for agent failures, and the prompt forbids substituting invented product facts.
- Invalid requests: FastAPI returns a clear validation response; invalid product/page references return a not-found response; database failures return a temporary-unavailable response.

## Audit Trail

`output/audit_trail.json` is a JSON array used as a logical append-only audit trail. A new `/chat` run does not clear earlier entries. Each run records:

- `time`: UTC timestamp in ISO 8601 format.
- `run_id`: identifier shared by all events in one agent run.
- `event`: `run_start`, `tool_call`, or `run_stop`.
- `tool_name`: `agent_loop`, `search_products`, or `get_product_details` as applicable.
- `args`: concise, redacted arguments such as the user query or product ID.
- `result`: concise response/tool output or an error record.
- `stop_reason`: `started`, `tool_completed`, `tool_error`, the model finish reason, or `error`.

The `/chat` route starts and stops the audit record around `shop_agent.run`. The catalogue functions record their actual tool calls while an agent run is active. The file is read, appended to, and written back with all prior entries preserved, so repeated agent runs accumulate evidence of what the agent actually did.

## API and Application Routes

- `GET /api/health`: service health check.
- `POST /chat`: guest or logged-in agent chat with structured `ChatReply` output.
- `GET /api/chat/history/{user_id}?email=...`: load validated logged-in chat history.
- `GET /api/products`: return the catalogue for the Products page.
- `GET /api/products/{product_id}`: return one product and its inventory.
- `GET /api/product-categories`: return shopper-friendly grouped categories.
- `GET /api/woofs/{user_id}?email=...`: load a logged-in shopper’s saved products.
- `POST /api/woofs`: toggle a product in or out of “Your Woofs.” Guests are rejected.
- `POST /api/auth/register`: create an account with a securely hashed password.
- `POST /api/auth/login`: verify credentials and return only public user fields.
- `/images/...`: serve catalogue product images from the `data/` directory.

## How to Run and Test

From the project root, install frontend dependencies with `npm install`. Start the backend from `backend/` using its existing virtual environment:

```bash
cd backend
.venv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

The Vite proxy in `vite.config.ts` sends `/api`, `/images`, and `/chat` to port `8001`. In a second terminal from the project root, start the frontend:

```bash
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`. Verify the backend independently with `curl http://127.0.0.1:8001/api/health`. A product chat test can be sent with:

```bash
curl -X POST http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"What hoodies do you have?","conversation":[]}'
```

Run `npm run build` to type-check and build the frontend. For backend dependencies, use `cd backend && .venv/bin/python -m pip install -r requirements.txt`. If port `8001` is unavailable, run the API on another port and update the three Vite proxy targets to match; port `8000` is also supported by the FastAPI app.
