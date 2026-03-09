from sqlalchemy.orm import Session
from app.models.demand import Demand
from app.models.harvest import Harvest
from app.models.location_model import UserLocation

def generate_heatmap_data(db: Session, crop: str):
    # Fetch all open demands for the crop with their locations
    active_demands = (
        db.query(UserLocation.latitude, UserLocation.longitude)
        .join(Demand, Demand.vendor_id == UserLocation.user_id)
        .filter(Demand.crop_type.ilike(f"%{crop}%"))
        .filter(Demand.status == "open")
        .all()
    )

    # Fetch all available harvests for the crop with their locations
    available_harvests = (
        db.query(UserLocation.latitude, UserLocation.longitude)
        .join(Harvest, Harvest.farmer_id == UserLocation.user_id)
        .filter(Harvest.crop_type.ilike(f"%{crop}%"))
        .filter(Harvest.status == "available")
        .all()
    )

    # Grid size: rounding to 2 decimal places is approx 1.1km grid aggregation
    heatmap_grid = {}

    for lat, lng in active_demands:
        if lat is None or lng is None:
            continue
        grid_key = (round(lat, 2), round(lng, 2))
        if grid_key not in heatmap_grid:
            heatmap_grid[grid_key] = {"demand_count": 0, "harvest_count": 0}
        heatmap_grid[grid_key]["demand_count"] += 1

    for lat, lng in available_harvests:
        if lat is None or lng is None:
            continue
        grid_key = (round(lat, 2), round(lng, 2))
        if grid_key not in heatmap_grid:
            heatmap_grid[grid_key] = {"demand_count": 0, "harvest_count": 0}
        heatmap_grid[grid_key]["harvest_count"] += 1

    heatmap_points = []
    for (lat, lng), counts in heatmap_grid.items():
        # Demand score calculation for the cell
        demand_score = (counts["demand_count"] * 2) - counts["harvest_count"]
        # Floor to 0 so we don't have negative heat
        demand_score = max(0, demand_score)
        
        heatmap_points.append({
            "lat": lat,
            "lng": lng,
            "demand_score": demand_score,
            "demand_count": counts["demand_count"],
            "harvest_count": counts["harvest_count"]
        })

    return heatmap_points
