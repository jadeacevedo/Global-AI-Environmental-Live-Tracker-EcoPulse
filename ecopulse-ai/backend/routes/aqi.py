"""Air Quality API router."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_aqi(request: Request):
    """Get current AQI metrics from shared app state."""
    return request.app.state.data.get("aqi", {})
