from sqlalchemy.orm import Session
from app.models.price_history import PriceHistory


def calculate_price_change(db: Session, crop_type: str):
    prices = (
        db.query(PriceHistory)
        .filter(PriceHistory.crop_type == crop_type)
        .order_by(PriceHistory.created_at.desc())
        .limit(2)
        .all()
    )

    if len(prices) < 2:
        return {"change_percent": 0}

    latest = prices[0].price
    previous = prices[1].price

    if previous == 0:
        return {"change_percent": 0}

    change = ((latest - previous) / previous) * 100

    return {
        "latest_price": latest,
        "previous_price": previous,
        "change_percent": round(change, 2)
    }
