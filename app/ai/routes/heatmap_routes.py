from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.ai.services.heatmap_service import generate_heatmap_data

router = APIRouter(prefix="/ai", tags=["AI Heatmap"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/heatmap")
def crop_heatmap(crop: str, db: Session = Depends(get_db)):
    data = generate_heatmap_data(db, crop)
    return {
        "crop": crop,
        "heatmap": data
    }
