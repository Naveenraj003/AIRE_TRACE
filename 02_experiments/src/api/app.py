from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from src.api.loaders import load_and_validate_artifacts, get_state
from src.api.routes import episodes, predictions, evaluation, audit, investigation
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load and validate on startup
    load_and_validate_artifacts()
    yield

app = FastAPI(title="AIRE-Trace Read-Only API", lifespan=lifespan)

# Mount API routes
app.include_router(episodes.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")
app.include_router(evaluation.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
app.include_router(investigation.router, prefix="/api")

@app.get("/api/health")
def health():
    return get_state()

# Mount frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

