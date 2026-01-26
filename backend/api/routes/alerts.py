"""Alert management endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.preferences import (
    Alert,
    AlertCheck,
    AlertCreate,
    AlertResponse,
)
from services.stock_service import fetch_stock_data

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertResponse])
async def get_alerts(
    active_only: bool = True, db: Session = Depends(get_db)
) -> list[AlertResponse]:
    """Get all alerts."""
    query = db.query(Alert)
    if active_only:
        query = query.filter(Alert.is_active == True)
    return query.all()


@router.post("/", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Create a new price alert."""
    valid_types = ["price_above", "price_below", "percent_change"]
    if alert.alert_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid alert_type. Must be one of: {valid_types}",
        )

    db_alert = Alert(
        symbol=alert.symbol.upper(),
        alert_type=alert.alert_type,
        target_value=alert.target_value,
        notes=alert.notes,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a specific alert."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.delete("/{alert_id}")
async def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()
    return {"message": f"Alert {alert_id} deleted"}


@router.post("/{alert_id}/deactivate", response_model=AlertResponse)
async def deactivate_alert(alert_id: int, db: Session = Depends(get_db)):
    """Deactivate an alert without deleting it."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_active = False
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/check/all", response_model=list[AlertCheck])
async def check_all_alerts(db: Session = Depends(get_db)):
    """Check all active alerts and return their status."""
    alerts = db.query(Alert).filter(Alert.is_active == True).all()
    results = []

    for alert in alerts:
        try:
            stock_data = fetch_stock_data(alert.symbol)
            current_price = stock_data.price if stock_data else None
        except Exception:
            current_price = None

        should_trigger = False
        message = ""

        if current_price is None:
            message = f"Could not fetch price for {alert.symbol}"
        elif alert.alert_type == "price_above":
            if current_price >= alert.target_value:
                should_trigger = True
                message = f"{alert.symbol} is at ${current_price:.2f}, above target ${alert.target_value:.2f}"
            else:
                message = f"{alert.symbol} is at ${current_price:.2f}, below target ${alert.target_value:.2f}"
        elif alert.alert_type == "price_below":
            if current_price <= alert.target_value:
                should_trigger = True
                message = f"{alert.symbol} is at ${current_price:.2f}, below target ${alert.target_value:.2f}"
            else:
                message = f"{alert.symbol} is at ${current_price:.2f}, above target ${alert.target_value:.2f}"
        elif alert.alert_type == "percent_change":
            # For percent_change, we'd need a reference price
            # This is a simplified implementation
            message = f"Percent change alerts require price history (not yet implemented)"

        # Update alert if triggered
        if should_trigger and not alert.is_triggered:
            alert.is_triggered = True
            alert.triggered_at = datetime.utcnow()
            db.commit()
            db.refresh(alert)

        results.append(
            AlertCheck(
                alert=AlertResponse.model_validate(alert),
                current_price=current_price,
                should_trigger=should_trigger,
                message=message,
            )
        )

    return results


@router.get("/symbol/{symbol}", response_model=list[AlertResponse])
async def get_alerts_for_symbol(
    symbol: str, active_only: bool = True, db: Session = Depends(get_db)
):
    """Get all alerts for a specific symbol."""
    query = db.query(Alert).filter(Alert.symbol == symbol.upper())
    if active_only:
        query = query.filter(Alert.is_active == True)
    return query.all()
