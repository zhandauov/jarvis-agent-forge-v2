from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.prompt_seeder import seed_default_prompts
from core.database import create_tables
from knowledge_base.store import KBStore
from models import slide_config as _slide_config_model  # noqa: F401 — ensures table is registered
from routers import reports, chapters, agent_configs, knowledge_base, generation, websocket, auth, prompts, slides


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await seed_default_prompts()
    await KBStore.instance().reload_from_db()
    yield


app = FastAPI(title="Consulting Platform API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:80", "http://frontend"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(chapters.router)
app.include_router(agent_configs.router)
app.include_router(knowledge_base.router)
app.include_router(generation.router)
app.include_router(websocket.router)
app.include_router(prompts.router)
app.include_router(slides.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
