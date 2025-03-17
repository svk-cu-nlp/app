from fastapi import FastAPI
from api.routes import summary, features

app = FastAPI(
    title="SRS Analysis API",
    description="API for analyzing Software Requirements Specification documents",
    version="1.0.0"
)

# Include routers
app.include_router(summary.router)
app.include_router(features.router)

@app.get("/")
async def root():
    return {"message": "Welcome to SRS Analysis API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)