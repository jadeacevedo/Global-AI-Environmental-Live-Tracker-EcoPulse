"""
EcoPulse AI — Backend API
FastAPI server that aggregates live environmental and AI usage data.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from collectors.carbon import CarbonCollector
from collectors.air_quality import AirQualityCollector
from collectors.inference import InferenceEstimator
from collectors.water import WaterStressCollector
from collectors.trends import TrendsCollector
from routes import carbon, aqi, inference, water, summary

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── Shared state (in-memory cache, updated by background tasks) ──────────────
state: dict = {
    "carbon": {},
    "aqi": {},
    "inference": {},
    "water": {},
    "trends": {},
    "last_updated": None,
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start background refresh tasks on startup."""
    collectors = [
        CarbonCollector(state),
        AirQualityCollector(state),
        InferenceEstimator(state),
        WaterStressCollector(state),
        TrendsCollector(state),
    ]
    tasks = [asyncio.create_task(c.run()) for c in collectors]
    logger.info("✅ All background collectors started.")
    yield
    for t in tasks:
        t.cancel()
    logger.info("🛑 Collectors shut down.")

app = FastAPI(
    title="EcoPulse AI",
    description="Real-time AI environmental impact tracker",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Inject shared state into routers ─────────────────────────────────────────
app.state.data = state

# ── Register routers ─────────────────────────────────────────────────────────
app.include_router(carbon.router,    prefix="/api/carbon",    tags=["Carbon"])
app.include_router(aqi.router,       prefix="/api/aqi",       tags=["Air Quality"])
app.include_router(inference.router, prefix="/api/inference", tags=["Inference"])
app.include_router(water.router,     prefix="/api/water",     tags=["Water"])
app.include_router(summary.router,   prefix="/api/summary",   tags=["Summary"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "last_updated": state.get("last_updated")}

@app.get("/")
async def root():
    return {"status": "ok", "service": "EcoPulse AI", "ready": True}


@app.get("/api/live")
async def live_snapshot(request_obj: None = None):
    """Single endpoint returning all current metrics — used by the dashboard."""
    from datetime import datetime, timezone
    return JSONResponse({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "carbon":    state.get("carbon", {}),
        "aqi":       state.get("aqi", {}),
        "inference": state.get("inference", {}),
        "water":     state.get("water", {}),
        "trends":    state.get("trends", {}),
    })
