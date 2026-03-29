"""Carbon API router."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_carbon(request: Request):
    return request.app.state.data.get("carbon", {})
