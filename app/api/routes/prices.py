from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.price_service import calculate_price_change

router = APIRouter(prefix="/prices", tags=["Prices"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{crop_type}")
def get_price_trend(crop_type: str, db: Session = Depends(get_db)):
    return calculate_price_change(db, crop_type)
