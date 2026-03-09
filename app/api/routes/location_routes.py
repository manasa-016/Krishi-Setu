from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# These imports will succeed once the plugin is merged into Agritech-b
from app.core.database import SessionLocal
from app.core.security import get_current_user

from app.schemas.location_schema import (
    LocationUpdate, LocationListResponse, 
    HarvestLocationListResponse, DemandLocationListResponse, MarketMapResponse
)
from app.services import location_service

router = APIRouter(prefix="/location", tags=["Location"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/update")
def update_location(
    location: LocationUpdate,
    current_user=Depends(get_current_user),
    db: Session=Depends(get_db)
):
    location_service.update_user_location(
        db=db, 
        user_id=current_user.id, 
        latitude=location.latitude, 
        longitude=location.longitude
    )
    return {"message": "Location updated successfully"}


@router.get("/vendors", response_model=LocationListResponse)
def get_vendors(db: Session=Depends(get_db)):
    vendors = location_service.get_users_by_role(db, "vendor")
    return {"results": vendors}


@router.get("/farmers", response_model=LocationListResponse)
def get_farmers(db: Session=Depends(get_db)):
    farmers = location_service.get_users_by_role(db, "farmer")
    return {"results": farmers}


@router.get("/vendors-nearby")
def vendors_nearby(lat: float, lng: float, radius: float, db: Session = Depends(get_db)):
    vendors = location_service.find_nearby_users(db, "vendor", lat, lng, radius)
    return {"vendors": vendors}


@router.get("/farmers-nearby")
def farmers_nearby(lat: float, lng: float, radius: float, db: Session = Depends(get_db)):
    farmers = location_service.find_nearby_users(db, "farmer", lat, lng, radius)
    return {"farmers": farmers}


@router.get("/harvests-nearby", response_model=HarvestLocationListResponse)
def harvests_nearby(lat: float, lng: float, radius: float, db: Session = Depends(get_db)):
    harvests = location_service.find_nearby_harvests(db, lat, lng, radius)
    return {"harvests": harvests}


@router.get("/demands-nearby", response_model=DemandLocationListResponse)
def demands_nearby(lat: float, lng: float, radius: float, db: Session = Depends(get_db)):
    demands = location_service.find_nearby_demands(db, lat, lng, radius)
    return {"demands": demands}


@router.get("/market-map", response_model=MarketMapResponse)
def market_map(lat: float, lng: float, radius: float, db: Session = Depends(get_db)):
    return {
        "vendors": location_service.find_nearby_users(db, "vendor", lat, lng, radius),
        "farmers": location_service.find_nearby_users(db, "farmer", lat, lng, radius),
        "harvests": location_service.find_nearby_harvests(db, lat, lng, radius),
        "demands": location_service.find_nearby_demands(db, lat, lng, radius)
    }
