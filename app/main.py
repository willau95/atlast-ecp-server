"""
ATLAST ECP Server — Evidence Chain Protocol Backend

Handles:
- EAS on-chain anchoring (hourly cron)
- Webhook dispatch to LLaChat
- .well-known/ecp.json discovery
- Health check
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    print(f"ECP Server starting. EAS_CHAIN={settings.EAS_CHAIN}, STUB={settings.EAS_STUB_MODE}")
    yield
    print("ECP Server shutting down.")


app = FastAPI(
    title="ATLAST ECP Server",
    description="Evidence Chain Protocol — EAS anchoring and webhook dispatch",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
from .routes.health import router as health_router
from .routes.discovery import router as discovery_router
from .routes.anchor import router as anchor_router

app.include_router(health_router)
app.include_router(discovery_router)
app.include_router(anchor_router)
