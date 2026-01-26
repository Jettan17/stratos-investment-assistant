"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Check API health status."""
    return {
        "status": "healthy",
        "version": "0.1.0",
    }
