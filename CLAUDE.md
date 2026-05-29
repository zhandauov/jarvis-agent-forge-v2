# CLAUDE.md

# User notes
If a user wants to add or do something in plan mode and suggests a way to achieve a solution, consider whether there are better ways to achieve this goal or solve the problem in other, more effective or better ways and suggest it.

## Project Overview

Multi-agent consulting report generation platform. Users define reports with chapters, configure AI agent teams (supervisor + workers), upload knowledge base documents, and trigger generation runs. Agents collaborate via a supervisor-worker pattern to research and write chapter content, streaming results in real time.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy (async), aiosqlite, Anthropic SDK
- **Frontend**: Vue 3 + TypeScript, Vite, Pinia, Vue Router, Axios
- **AI**: Claude (`claude-sonnet-4-6` default), multi-agent orchestration
- **Deployment**: Docker Compose (nginx + uvicorn)

## Development Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
# Copy and fill in .env.example → .env
uvicorn main:app --reload        # dev server on :8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                      # Vite dev server on :5173 (proxies to :8000)
npm run build                    # type-check + production build
npm run type-check               # vue-tsc only
```

### Docker (full stack)
```bash
docker-compose up --build        # backend :8000, frontend :80
```

### No test suite exists in this project.

## Shell Environment

This project runs on Windows. Use the **Bash tool** for all shell commands (file listing, running servers, git, npm, pip). Do **not** use PowerShell-only commands like `Get-ChildItem`, `Set-Location`, `Select-String`, etc. — they fail in the Bash tool context. Stick to POSIX commands: `ls`, `cd`, `grep`, `find`, `cat`.

## Architecture

### Multi-Agent Generation Flow

The core logic lives in [backend/agents/](backend/agents/):

1. `orchestrator.py` — entry point for generation runs; limits concurrency to 2 via asyncio `Semaphore`
2. `supervisor.py` — `SupervisorAgent` drives the full loop: **Plan → Dispatch Workers → Review → (optional discussion rounds) → Aggregate**
3. `worker.py` — `WorkerAgent` receives a task, searches the KB, calls Claude, returns a `WorkerResult`
4. `message_bus.py` — in-process `asyncio.Queue`; all agent events are published here and consumed by the WebSocket router
5. `models.py` — dataclasses (`WorkerTask`, `PlanResult`, `WorkerResult`, `SupervisorDecision`) shared between agents
6. `prompts.py` — all system/user prompt templates (edit here to change agent behavior)

### Knowledge Base (RAG)

[backend/knowledge_base/](backend/knowledge_base/): PDF/DOCX files are uploaded, extracted to text, chunked (200–800 chars), and stored in an in-memory token-based index (`store.py`). The KB is reloaded from disk on startup (see `main.py` lifespan).

### API Layer

[backend/routers/](backend/routers/) — 8 FastAPI routers mounted in `main.py`:
- `auth.py` — JWT login
- `reports.py`, `chapters.py`, `agent_configs.py` — CRUD
- `knowledge_base.py` — file upload/delete
- `generation.py` — trigger runs, poll status
- `websocket.py` — `GET /ws/runs/{run_id}` streams `AgentMessage` events as JSON

### Frontend Data Flow

- **Pinia stores** ([frontend/src/stores/](frontend/src/stores/)) own all server state; views call store actions, not the API modules directly.
- **`generation.ts` store** opens a WebSocket via `useWebSocket.ts` composable and appends incoming messages to local state — this is what drives the live agent conversation UI.
- **Route guard** in [frontend/src/router/index.ts](frontend/src/router/index.ts) validates the JWT and redirects to `/login` if missing or expired.
- API proxy: Vite dev server proxies `/api` and `/ws` to `http://localhost:8000` ([frontend/vite.config.ts](frontend/vite.config.ts)).

### Database

SQLite via async SQLAlchemy. Schema: `Report → Chapter → GenerationRun → AgentMessage`, plus `AgentTeamConfig` and `KBDocument`. Tables are created on startup in `core/database.py`.

### Auth

JWT Bearer tokens. `core/dependencies.py` exports `get_current_user` used as a FastAPI dependency. Token secrets configured via `AUTH_SECRET_KEY` env var.

## Key Configuration

Backend env vars (see [.env.example](.env.example)):

| Variable | Default | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `DATABASE_URL` | `sqlite+aiosqlite:////app/data/consulting.db` | |
| `DEFAULT_MODEL` | `claude-sonnet-4-6` | Per-config override possible |
| `MAX_UPLOAD_MB` | `50` | KB file size limit |
