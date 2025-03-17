from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import summary

app = FastAPI(
    title="SRS Analysis API",
    description="API for analyzing Software Requirements Specification documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(summary.router)
