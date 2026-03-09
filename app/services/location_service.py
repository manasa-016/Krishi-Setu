from sqlalchemy.orm import Session
from app.models.location_model import UserLocation

# We assume this will be merged and have access to app.models.user
from app.models.user import User

def update_user_location(db: Session, user_id: str, latitude: float, longitude: float):
    # Upsert logic: Update if exists, else Insert
    location = db.query(UserLocation).filter(UserLocation.user_id == user_id).first()
    
    if location:
        location.latitude = latitude
        location.longitude = longitude
    else:
        location = UserLocation(user_id=user_id, latitude=latitude, longitude=longitude)
        db.add(location)
        
    db.commit()
    return location

def get_users_by_role(db: Session, role: str):
    # Join users with user_locations to get active coordinates for the given role
    results = (
        db.query(User.id, User.name, UserLocation.latitude, UserLocation.longitude)
        .join(UserLocation, User.id == UserLocation.user_id)
        .filter(User.role == role)
        .all()
    )
    
    return [
        {
            "id": str(r.id),
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude
        }
        for r in results
    ]


from app.utils.distance import haversine_distance

def find_nearby_users(db: Session, role: str, lat: float, lng: float, radius_km: float):
    distance = haversine_distance(
        lat,
        lng,
        UserLocation.latitude,
        UserLocation.longitude
    )

    results = (
        db.query(
            User.id,
            User.name,
            UserLocation.latitude,
            UserLocation.longitude,
            distance.label("distance_km")
        )
        .join(UserLocation, User.id == UserLocation.user_id)
        .filter(User.role == role)
        .filter(distance <= radius_km)
        .order_by(distance)
        .limit(50)
        .all()
    )

    return [
        {
            "id": str(r.id),
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "distance_km": round(r.distance_km, 2) if r.distance_km else 0.0
        }
        for r in results
    ]


# We assume this will be merged and have access to app.models.harvest
from app.models.harvest import Harvest

def find_nearby_harvests(db: Session, lat: float, lng: float, radius_km: float):
    distance = haversine_distance(
        lat,
        lng,
        UserLocation.latitude,
        UserLocation.longitude
    )

    results = (
        db.query(
            User.id.label("farmer_id"),
            User.name.label("farmer_name"),
            Harvest.crop_type,
            Harvest.quantity,
            Harvest.price_per_kg,
            UserLocation.latitude,
            UserLocation.longitude,
            distance.label("distance_km")
        )
        .join(UserLocation, User.id == UserLocation.user_id)
        .join(Harvest, Harvest.farmer_id == User.id)
        .filter(User.role == "farmer")
        .filter(Harvest.status == "available")
        .filter(distance <= radius_km)
        .order_by(distance)
        .limit(50)
        .all()
    )

    return [
        {
            "farmer_id": str(r.farmer_id),
            "farmer_name": r.farmer_name,
            "crop_type": r.crop_type,
            "quantity": r.quantity,
            "price_per_kg": r.price_per_kg,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "distance_km": round(r.distance_km, 2) if r.distance_km else 0.0
        }
        for r in results
    ]


from app.models.demand import Demand

def find_nearby_demands(db: Session, lat: float, lng: float, radius_km: float):
    distance = haversine_distance(
        lat,
        lng,
        UserLocation.latitude,
        UserLocation.longitude
    )

    results = (
        db.query(
            User.id.label("vendor_id"),
            User.name.label("vendor_name"),
            Demand.crop_type,
            Demand.required_quantity,
            Demand.offered_price,
            UserLocation.latitude,
            UserLocation.longitude,
            distance.label("distance_km")
        )
        .join(UserLocation, User.id == UserLocation.user_id)
        .join(Demand, Demand.vendor_id == User.id)
        .filter(User.role == "vendor")
        .filter(Demand.status == "open")
        .filter(distance <= radius_km)
        .order_by(distance)
        .limit(50)
        .all()
    )

    return [
        {
            "vendor_id": str(r.vendor_id),
            "vendor_name": r.vendor_name,
            "crop_type": r.crop_type,
            "required_quantity": r.required_quantity,
            "offered_price": r.offered_price,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "distance_km": round(r.distance_km, 2) if r.distance_km else 0.0
        }
        for r in results
    ]
