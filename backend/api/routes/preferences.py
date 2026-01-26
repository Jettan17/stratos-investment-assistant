"""User preferences and watchlist endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.preferences import (
    PreferencesCreate,
    PreferencesResponse,
    UserPreferences,
    Watchlist,
    WatchlistItemCreate,
    WatchlistItemResponse,
)

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.get("/", response_model=PreferencesResponse)
async def get_preferences(
    name: str = "default",
    db: Session = Depends(get_db),
):
    """Get user screening preferences by name."""
    prefs = db.query(UserPreferences).filter(UserPreferences.name == name).first()

    if not prefs:
        # Return default preferences if none exist
        prefs = UserPreferences(
            name=name,
            min_dividend_yield=2.0,
            max_pe_ratio=25.0,
            min_market_cap=10.0,
            max_beta=1.0,
            preferred_sectors=[],
        )
        db.add(prefs)
        db.commit()
        db.refresh(prefs)

    return prefs


@router.post("/", response_model=PreferencesResponse)
async def save_preferences(
    preferences: PreferencesCreate,
    db: Session = Depends(get_db),
):
    """Save or update user screening preferences."""
    existing = (
        db.query(UserPreferences)
        .filter(UserPreferences.name == preferences.name)
        .first()
    )

    if existing:
        # Update existing
        existing.min_dividend_yield = preferences.min_dividend_yield
        existing.max_pe_ratio = preferences.max_pe_ratio
        existing.min_market_cap = preferences.min_market_cap
        existing.max_beta = preferences.max_beta
        existing.max_debt_to_equity = preferences.max_debt_to_equity
        existing.preferred_sectors = preferences.preferred_sectors
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new
        prefs = UserPreferences(
            name=preferences.name,
            min_dividend_yield=preferences.min_dividend_yield,
            max_pe_ratio=preferences.max_pe_ratio,
            min_market_cap=preferences.min_market_cap,
            max_beta=preferences.max_beta,
            max_debt_to_equity=preferences.max_debt_to_equity,
            preferred_sectors=preferences.preferred_sectors,
        )
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
        return prefs


@router.delete("/{name}")
async def delete_preferences(
    name: str,
    db: Session = Depends(get_db),
):
    """Delete user preferences by name."""
    prefs = db.query(UserPreferences).filter(UserPreferences.name == name).first()

    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")

    db.delete(prefs)
    db.commit()
    return {"message": f"Preferences '{name}' deleted"}


# Watchlist endpoints
watchlist_router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@watchlist_router.get("/", response_model=list[WatchlistItemResponse])
async def get_watchlist(
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    """Get user's stock watchlist."""
    query = db.query(Watchlist)
    if active_only:
        query = query.filter(Watchlist.is_active == True)
    return query.all()


@watchlist_router.post("/", response_model=WatchlistItemResponse)
async def add_to_watchlist(
    item: WatchlistItemCreate,
    db: Session = Depends(get_db),
):
    """Add a stock to the watchlist."""
    existing = (
        db.query(Watchlist)
        .filter(Watchlist.symbol == item.symbol.upper())
        .first()
    )

    if existing:
        # Reactivate if inactive
        existing.is_active = True
        existing.notes = item.notes
        existing.target_price = item.target_price
        db.commit()
        db.refresh(existing)
        return existing

    watchlist_item = Watchlist(
        symbol=item.symbol.upper(),
        notes=item.notes,
        target_price=item.target_price,
    )
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    return watchlist_item


@watchlist_router.delete("/{symbol}")
async def remove_from_watchlist(
    symbol: str,
    db: Session = Depends(get_db),
):
    """Remove a stock from the watchlist (soft delete)."""
    item = (
        db.query(Watchlist)
        .filter(Watchlist.symbol == symbol.upper())
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Stock not in watchlist")

    item.is_active = False
    db.commit()
    return {"message": f"{symbol.upper()} removed from watchlist"}
