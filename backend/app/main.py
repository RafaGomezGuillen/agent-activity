import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import agents, keylogs, metrics

app = FastAPI(
    title="Alisium Agent Activity API",
    description="""
    This API provides endpoints to manage and retrieve agent activity data for the Alisium project
    """,
    version="0.0.1",
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
    print("Starting AAA API... \nExecuting on http://127.0.0.1:8000\nDocs available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)

if __name__ == "__main__":
    run_app()