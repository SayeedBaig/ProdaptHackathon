from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.errors import setup_exception_handlers
from app.api.routes import (
    auth,
    startups,
    idea,
    analyses,
    pitch,
    investor,
    readiness,
    feedback,
    health,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="PitchPilot AI — Master Backend API for Startup Coaching, Pitch Generation, and Investor Simulation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Exception handlers with standard error envelope
setup_exception_handlers(app)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN, "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health routes (mounted globally)
app.include_router(health.router)

# API v1 Router
api_v1_router = APIRouter(prefix=settings.API_V1_PREFIX)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(startups.router)
api_v1_router.include_router(idea.router)
api_v1_router.include_router(analyses.router)
api_v1_router.include_router(pitch.router)
api_v1_router.include_router(investor.router)
api_v1_router.include_router(readiness.router)
api_v1_router.include_router(feedback.router)

app.include_router(api_v1_router)

# Mount also at /api for flexible frontend integration
api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(startups.router)
api_router.include_router(idea.router)
api_router.include_router(analyses.router)
api_router.include_router(pitch.router)
api_router.include_router(investor.router)
api_router.include_router(readiness.router)
api_router.include_router(feedback.router)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "health": "/health",
    }
