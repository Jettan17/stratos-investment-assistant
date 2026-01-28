"""Main FastAPI application for Stratos Investment Assistant."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, stocks
from api.routes.alerts import router as alerts_router
from api.routes.analysis import router as analysis_router
from api.routes.portfolio import router as portfolio_router
from api.routes.preferences import router as preferences_router
from api.routes.preferences import watchlist_router
from models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - runs on startup and shutdown."""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Stratos Investment Assistant API",
    description="Conservative long-term investment assistant for finding stable stocks",
    version="0.5.0",
    lifespan=lifespan,
)

# CORS configuration for frontend
# Allow Vercel frontend and localhost for development
cors_origins = [
    "http://localhost:3000",
    "https://frontend-omega-one-98.vercel.app",
]
# Add custom frontend URL from environment if set
if frontend_url := os.getenv("FRONTEND_URL"):
    cors_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(stocks.router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(portfolio_router, prefix="/api/v1")
app.include_router(preferences_router, prefix="/api/v1")
app.include_router(watchlist_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Stratos Investment Assistant API",
        "version": "0.5.0",
        "docs": "/docs",
        "endpoints": {
            "stocks": "/api/v1/stocks",
            "alerts": "/api/v1/alerts",
            "analysis": "/api/v1/analysis",
            "portfolio": "/api/v1/portfolio",
            "preferences": "/api/v1/preferences",
            "watchlist": "/api/v1/watchlist",
        },
    }
