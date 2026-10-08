from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


app = FastAPI(
    title="LegalEase API",
    version="1.0.0",
    description=(
        "AI-powered legal document "
        "drafting API."
    )
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.get("/")
def root():

    return {
        "name": "LegalEase API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


app.include_router(router)