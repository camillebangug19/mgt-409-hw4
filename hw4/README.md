# Campus Customs — HW4

Campus Customs is a React storefront for official Yale merchandise with a FastAPI/PydanticAI shopping assistant. The site supports catalogue browsing, product detail pages, account login, saved “Woofs,” database-grounded product chat, logged-in chat history, and an append-only agent audit trail.

## Local data pack

The local data pack is required to run the application but is intentionally not included in this submission. Place these local-only files under `hw4/data/` before starting the backend:

- `data/campus_customs.db`
- `data/products/`

The backend reads the SQLite database and product images from those paths. Do not commit the database, product images, `.env`, or API keys.

## Environment

Copy `.env.example` to `.env` at the `hw4/` root and set the `PORTKEY_API_KEY` value with your own key. The key is loaded from the environment and must never be committed.

## Backend

Create or activate a virtual environment in `backend/`, install the root requirements, and start FastAPI:

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

The API runs at `http://127.0.0.1:8000`. Its health check is `GET /api/health`. The backend expects the local data pack at `../data/` when launched from `backend/`.

## Frontend

In a second terminal, install and start the Vite frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`. The packaged Vite proxy sends `/api`, `/images`, and `/chat` requests to the backend on port `8000`.

## Documentation and checks

- `output/harness.md` documents the database, models, tools, safety rules, limits, API routes, audit trail, and run instructions.
- `output/app_check.html` presents the three Problem 11 live-site checks and links to their screenshots.
- `output/audit_trail.json` records agent run starts, catalogue tool calls, results, and stop reasons without clearing earlier entries.
- `AI_prompts.md` contains the homework prompt history.
