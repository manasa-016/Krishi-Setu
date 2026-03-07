from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.harvest import Harvest
from app.models.farm import Farm
from app.schemas.harvest_schema import HarvestCreate
from app.core.security import require_farmer, get_current_user
from app.services.distance_service import calculate_distance

router = APIRouter(prefix="/harvest", tags=["Harvest"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_harvest(
    harvest: HarvestCreate,
    current_user = Depends(require_farmer),
    db: Session = Depends(get_db)
):
    new_harvest = Harvest(
        farmer_id=current_user.id,
        crop_type=harvest.crop_type,
        category=harvest.category,
        quantity=harvest.quantity,
        price_per_kg=harvest.price_per_kg,
        description=harvest.description,
    )

    db.add(new_harvest)
    db.commit()
    db.refresh(new_harvest)

    return {"message": "Harvest created", "id": str(new_harvest.id)}


@router.get("/nearby/{lat}/{lng}")
def get_nearby_harvests(
    lat: float,
    lng: float,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    farms = db.query(Farm).all()
    harvests = db.query(Harvest).filter(Harvest.status == "available").all()

    nearby = []

    for harvest in harvests:
        farm = db.query(Farm).filter(Farm.farmer_id == harvest.farmer_id).first()

        if not farm:
            continue

        distance = calculate_distance(
            lat,
            lng,
            farm.location_lat,
            farm.location_lng,
        )

        if distance <= 10:
            nearby.append({
                "harvest_id": str(harvest.id),
                "crop_type": harvest.crop_type,
                "distance_km": round(distance, 2),
                "price": harvest.price_per_kg
            })

    return nearby


@router.get("/")
def list_harvests(db: Session = Depends(get_db)):
    harvests = db.query(Harvest).filter(Harvest.status == "available").all()

    return [
        {
            "id": str(h.id),
            "crop_type": h.crop_type,
            "category": h.category,
            "quantity": h.quantity,
            "price_per_kg": h.price_per_kg,
            "status": h.status,
        }
        for h in harvests
    ]
