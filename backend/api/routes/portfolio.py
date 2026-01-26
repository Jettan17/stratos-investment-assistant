"""Portfolio management endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.preferences import (
    PortfolioHolding,
    PortfolioHoldingCreate,
    PortfolioHoldingResponse,
    PortfolioHoldingUpdate,
    PortfolioHoldingWithValue,
    PortfolioSummary,
)
from services.stock_service import fetch_stock_data

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/", response_model=PortfolioSummary)
async def get_portfolio(db: Session = Depends(get_db)):
    """Get full portfolio with current values and summary."""
    holdings = db.query(PortfolioHolding).all()

    if not holdings:
        return PortfolioSummary(
            total_value=0.0,
            total_cost=0.0,
            total_gain_loss=0.0,
            total_gain_loss_percent=0.0,
            holdings_count=0,
            holdings=[],
        )

    holdings_with_value = []
    total_value = 0.0
    total_cost = 0.0

    for holding in holdings:
        cost = holding.shares * holding.purchase_price
        total_cost += cost

        # Fetch current price
        try:
            stock_data = fetch_stock_data(holding.symbol)
            current_price = stock_data.price if stock_data else None
            name = stock_data.name if stock_data else None
        except Exception:
            current_price = None
            name = None

        if current_price:
            current_value = holding.shares * current_price
            total_value += current_value
            gain_loss = current_value - cost
            gain_loss_percent = (gain_loss / cost) * 100 if cost > 0 else 0
        else:
            current_value = None
            gain_loss = None
            gain_loss_percent = None

        holdings_with_value.append(
            PortfolioHoldingWithValue(
                id=holding.id,
                symbol=holding.symbol,
                name=name,
                shares=holding.shares,
                purchase_price=holding.purchase_price,
                current_price=current_price,
                purchase_date=holding.purchase_date,
                notes=holding.notes,
                current_value=current_value,
                gain_loss=gain_loss,
                gain_loss_percent=gain_loss_percent,
            )
        )

    total_gain_loss = total_value - total_cost
    total_gain_loss_percent = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0

    return PortfolioSummary(
        total_value=total_value,
        total_cost=total_cost,
        total_gain_loss=total_gain_loss,
        total_gain_loss_percent=total_gain_loss_percent,
        holdings_count=len(holdings),
        holdings=holdings_with_value,
    )


@router.post("/holdings", response_model=PortfolioHoldingResponse)
async def add_holding(holding: PortfolioHoldingCreate, db: Session = Depends(get_db)):
    """Add a new holding to the portfolio."""
    db_holding = PortfolioHolding(
        symbol=holding.symbol.upper(),
        shares=holding.shares,
        purchase_price=holding.purchase_price,
        purchase_date=holding.purchase_date or datetime.utcnow(),
        notes=holding.notes,
    )
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding


@router.get("/holdings", response_model=list[PortfolioHoldingResponse])
async def get_holdings(db: Session = Depends(get_db)):
    """Get all portfolio holdings."""
    return db.query(PortfolioHolding).all()


@router.get("/holdings/{holding_id}", response_model=PortfolioHoldingWithValue)
async def get_holding(holding_id: int, db: Session = Depends(get_db)):
    """Get a specific holding with current value."""
    holding = db.query(PortfolioHolding).filter(PortfolioHolding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    cost = holding.shares * holding.purchase_price

    try:
        stock_data = fetch_stock_data(holding.symbol)
        current_price = stock_data.price if stock_data else None
        name = stock_data.name if stock_data else None
    except Exception:
        current_price = None
        name = None

    if current_price:
        current_value = holding.shares * current_price
        gain_loss = current_value - cost
        gain_loss_percent = (gain_loss / cost) * 100 if cost > 0 else 0
    else:
        current_value = None
        gain_loss = None
        gain_loss_percent = None

    return PortfolioHoldingWithValue(
        id=holding.id,
        symbol=holding.symbol,
        name=name,
        shares=holding.shares,
        purchase_price=holding.purchase_price,
        current_price=current_price,
        purchase_date=holding.purchase_date,
        notes=holding.notes,
        current_value=current_value,
        gain_loss=gain_loss,
        gain_loss_percent=gain_loss_percent,
    )


@router.put("/holdings/{holding_id}", response_model=PortfolioHoldingResponse)
async def update_holding(
    holding_id: int, update: PortfolioHoldingUpdate, db: Session = Depends(get_db)
):
    """Update a portfolio holding."""
    holding = db.query(PortfolioHolding).filter(PortfolioHolding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    if update.shares is not None:
        holding.shares = update.shares
    if update.purchase_price is not None:
        holding.purchase_price = update.purchase_price
    if update.purchase_date is not None:
        holding.purchase_date = update.purchase_date
    if update.notes is not None:
        holding.notes = update.notes

    db.commit()
    db.refresh(holding)
    return holding


@router.delete("/holdings/{holding_id}")
async def delete_holding(holding_id: int, db: Session = Depends(get_db)):
    """Delete a portfolio holding."""
    holding = db.query(PortfolioHolding).filter(PortfolioHolding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    db.delete(holding)
    db.commit()
    return {"message": f"Holding {holding_id} deleted"}
