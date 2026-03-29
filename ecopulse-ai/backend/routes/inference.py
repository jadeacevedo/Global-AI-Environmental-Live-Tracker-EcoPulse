"""Inference API router."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_inference(request: Request):
    return request.app.state.data.get("inference", {})
