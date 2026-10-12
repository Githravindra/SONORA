from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.health import router as health_router
from app.api.routes.library import router as library_router
from app.api.routes.playlists import router as playlists_router
from app.api.routes.search import router as search_router
from app.api.routes.playback import router as playback_router
from app.api.routes.discovery import router as discovery_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.settings import router as settings_router
from app.core.config import settings
from app.db.session import init_db

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="SONORA backend API for premium music streaming",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event() -> None:
    init_db()

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(catalog_router, prefix="/api/v1")
app.include_router(playlists_router, prefix="/api/v1")
app.include_router(library_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(playback_router, prefix="/api/v1")
app.include_router(discovery_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")

@app.get("/")
def root() -> dict:
    return {"message": "SONORA backend is running"}
