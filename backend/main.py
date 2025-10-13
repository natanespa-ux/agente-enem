
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlmodel import SQLModel, create_engine
from . import models
from .routers import webhooks, optout, leads, ai_agent

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

app = FastAPI(title="Atendente ENEM API")

# Include routers
app.include_router(webhooks.api_router, prefix="/api")
app.include_router(optout.api_router, prefix="/api")
app.include_router(leads.api_router, prefix="/api")
app.include_router(ai_agent.api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Create database tables (sync migration recommended in prod - Alembic)
    from sqlmodel import SQLModel
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/api/health")
async def health():
    return {"status":"healthy"}
