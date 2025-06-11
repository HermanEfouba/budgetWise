from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import models
from database import engine
from routes import auth, budget, expenses, revenues, categories, tags

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BudgetWise API",
    description="A comprehensive budget management application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(budget.router)
app.include_router(expenses.router)
app.include_router(revenues.router)
app.include_router(categories.router)
app.include_router(tags.router)

# Serve static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("../frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)