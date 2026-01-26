"""User preferences and watchlist models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String

from models.database import Base


class UserPreferences(Base):
    """SQLAlchemy model for user screening preferences."""

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="default", unique=True)
    min_dividend_yield = Column(Float, nullable=True)
    max_pe_ratio = Column(Float, nullable=True)
    min_market_cap = Column(Float, nullable=True)
    max_beta = Column(Float, nullable=True)
    max_debt_to_equity = Column(Float, nullable=True)
    preferred_sectors = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Watchlist(Base):
    """SQLAlchemy model for user watchlist."""

    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    target_price = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)


class CachedStock(Base):
    """SQLAlchemy model for cached stock data."""

    __tablename__ = "cached_stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    price = Column(Float)
    dividend_yield = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    beta = Column(Float, nullable=True)
    debt_to_equity = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)


class PortfolioHolding(Base):
    """SQLAlchemy model for portfolio holdings."""

    __tablename__ = "portfolio_holdings"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    shares = Column(Float)
    purchase_price = Column(Float)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Pydantic schemas for API
class PreferencesCreate(BaseModel):
    """Schema for creating preferences."""

    name: str = "default"
    min_dividend_yield: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    min_market_cap: Optional[float] = None
    max_beta: Optional[float] = None
    max_debt_to_equity: Optional[float] = None
    preferred_sectors: list[str] = []


class PreferencesResponse(BaseModel):
    """Schema for preferences response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    min_dividend_yield: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    min_market_cap: Optional[float] = None
    max_beta: Optional[float] = None
    max_debt_to_equity: Optional[float] = None
    preferred_sectors: list[str] = []
    created_at: datetime
    updated_at: datetime


class WatchlistItemCreate(BaseModel):
    """Schema for adding to watchlist."""

    symbol: str
    notes: Optional[str] = None
    target_price: Optional[float] = None


class WatchlistItemResponse(BaseModel):
    """Schema for watchlist item response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    added_at: datetime
    notes: Optional[str] = None
    target_price: Optional[float] = None
    is_active: bool


class PortfolioHoldingCreate(BaseModel):
    """Schema for adding a portfolio holding."""

    symbol: str
    shares: float
    purchase_price: float
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None


class PortfolioHoldingUpdate(BaseModel):
    """Schema for updating a portfolio holding."""

    shares: Optional[float] = None
    purchase_price: Optional[float] = None
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None


class PortfolioHoldingResponse(BaseModel):
    """Schema for portfolio holding response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    shares: float
    purchase_price: float
    purchase_date: datetime
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PortfolioSummary(BaseModel):
    """Schema for portfolio summary with calculated metrics."""

    total_value: float
    total_cost: float
    total_gain_loss: float
    total_gain_loss_percent: float
    holdings_count: int
    holdings: list["PortfolioHoldingWithValue"]


class PortfolioHoldingWithValue(BaseModel):
    """Schema for portfolio holding with current value."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    name: Optional[str] = None
    shares: float
    purchase_price: float
    current_price: Optional[float] = None
    purchase_date: datetime
    notes: Optional[str] = None
    current_value: Optional[float] = None
    gain_loss: Optional[float] = None
    gain_loss_percent: Optional[float] = None


class Alert(Base):
    """SQLAlchemy model for price alerts."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    alert_type = Column(String)  # "price_above", "price_below", "percent_change"
    target_value = Column(Float)
    is_active = Column(Boolean, default=True)
    is_triggered = Column(Boolean, default=False)
    triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)


class AlertCreate(BaseModel):
    """Schema for creating an alert."""

    symbol: str
    alert_type: str  # "price_above", "price_below", "percent_change"
    target_value: float
    notes: Optional[str] = None


class AlertResponse(BaseModel):
    """Schema for alert response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    alert_type: str
    target_value: float
    is_active: bool
    is_triggered: bool
    triggered_at: Optional[datetime] = None
    created_at: datetime
    notes: Optional[str] = None


class AlertCheck(BaseModel):
    """Schema for alert check result."""

    alert: AlertResponse
    current_price: Optional[float] = None
    should_trigger: bool
    message: str
