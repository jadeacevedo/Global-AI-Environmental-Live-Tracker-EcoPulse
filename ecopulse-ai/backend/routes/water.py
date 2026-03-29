"""Water API router."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_water(request: Request):
    return request.app.state.data.get("water", {})
