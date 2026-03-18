import os

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from main import run_all, run_one


app = FastAPI(
    title="AI Cloud Optimizer API",
    description="Simulation API for Cloud Auto Scaling using ML, RL, Deep RL",
    version="1.0"
)

API_KEY = os.getenv("API_KEY", "").strip()


def _allowed_origins() -> list[str]:

    origins = {
        "http://localhost:8501",
        "http://localhost:3000",
    }

    frontend_url = os.getenv("FRONTEND_URL", "").strip()
    if frontend_url:
        origins.add(frontend_url)

    raw_allowed = os.getenv("ALLOWED_ORIGINS", "").strip()
    if raw_allowed:
        for origin in raw_allowed.split(","):
            origin = origin.strip()
            if origin:
                origins.add(origin)

    return sorted(origins)


def require_api_key(x_api_key: str = Header(default="")) -> None:

    # If API_KEY is not configured, auth is disabled for local/dev ease.
    if not API_KEY:
        return

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# -------------------------
# CORS (for frontend later)
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# -------------------------
# Root / Health
# -------------------------

@app.get("/", tags=["Health"])
def root():
    return {"status": "API running"}


# -------------------------
# Run all strategies
# -------------------------

@app.get("/simulate", tags=["Simulation"])
def simulate(_: None = Depends(require_api_key)):

    results = run_all()

    return {
        "status": "ok",
        "results": results
    }


# -------------------------
# Run single strategy
# -------------------------

@app.get("/run/{name}", tags=["Simulation"])
def run_strategy(name: str, _: None = Depends(require_api_key)):

    result = run_one(name)

    return {
        "status": "ok",
        "strategy": name,
        "result": result
    }


# -------------------------
# List strategies
# -------------------------

@app.get("/strategies", tags=["Info"])
def strategies(_: None = Depends(require_api_key)):

    return {
        "strategies": [
            "STATIC",
            "THRESHOLD",
            "ML",
            "RL",
            "ADVANCED",
            "DEEP_RL"
        ]
    }