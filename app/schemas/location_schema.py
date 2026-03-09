from pydantic import BaseModel
from typing import List

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

class LocationResponse(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float

class LocationListResponse(BaseModel):
    results: List[LocationResponse]

class HarvestLocationResponse(BaseModel):
    farmer_id: str
    farmer_name: str
    crop_type: str
    quantity: float
    price_per_kg: float
    latitude: float
    longitude: float
    distance_km: float

class HarvestLocationListResponse(BaseModel):
    harvests: List[HarvestLocationResponse]

class DemandLocationResponse(BaseModel):
    vendor_id: str
    vendor_name: str
    crop_type: str
    required_quantity: float
    offered_price: float
    latitude: float
    longitude: float
    distance_km: float

class DemandLocationListResponse(BaseModel):
    demands: List[DemandLocationResponse]

class MarketMapResponse(BaseModel):
    vendors: List[LocationResponse]
    farmers: List[LocationResponse]
    harvests: List[HarvestLocationResponse]
    demands: List[DemandLocationResponse]
