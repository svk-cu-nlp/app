from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.summary import router as summary_router
from api.routes.features import router as features_router
from api.routes.risks import router as risks_router

app = FastAPI(
    title="SRS Analysis API",
    description="API for analyzing Software Requirements Specification documents",
    version="1.0.0"
)

# Configure CORS with specific origins
origins = [
    "http://localhost:3000",    # Next.js default port
    "http://localhost:5173",    # Vite default port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(summary_router)
app.include_router(features_router)
app.include_router(risks_router)

@app.get("/")
async def root():
    return {"message": "Welcome to SRS Analysis API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
