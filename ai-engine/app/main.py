import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pitch_coach_router

app = FastAPI(
    title="AI Startup Pitch Coach - AI Engine Service",
    description="""
    Production-ready AI Service for Group 6: AI Startup Pitch Coach (Prodapt Hackathon).
    Supports 9 core AI modules:
    1. Idea Analysis
    2. Clarification Questions
    3. Value Proposition
    4. Market Analysis
    5. Pitch Generation
    6. Pitch Critique
    7. Investor Questions
    8. Answer Evaluation
    9. Readiness Report
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for integration with Frontend/Backend services
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pitch_coach_router.router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "service": "AI Startup Pitch Coach - AI Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "contract_samples": "/contracts"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
