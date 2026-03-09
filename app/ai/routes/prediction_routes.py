from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.ai.services.prediction_service import calculate_crop_demand

router = APIRouter(prefix="/ai", tags=["AI"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/crop-demand")
def crop_demand(crop: str, db: Session = Depends(get_db)):
    result = calculate_crop_demand(db, crop)
    return result
