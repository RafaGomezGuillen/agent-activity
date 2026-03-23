import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.logging import setup_logging
from app.services.scheduler import start_scheduler, stop_scheduler
from app.routes import agents, keylogs, metrics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- START SCHEDULER LOGIC ---
    start_scheduler()
    
    yield

    # --- STOP SCHEDULER LOGIC ---
    stop_scheduler()

app = FastAPI(
    title="Alisium Agent Activity API",
    description="""
    This API provides endpoints to manage and retrieve agent activity data for the Alisium project
    """,
    version="0.0.1",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",  # Development Vite server
    "http://localhost",       # Docker frontend
    "http://localhost:80",    # Docker frontend port
    "http://frontend:80",    # Docker network
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(agents.router)
app.include_router(keylogs.router)
app.include_router(metrics.router)

def run_app():
    setup_logging()
    
    print("Starting AAA API... \nExecuting on http://127.0.0.1:8000\nDocs available at http://127.0.0.1:8000/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    run_app()