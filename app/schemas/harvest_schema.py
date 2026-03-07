from pydantic import BaseModel
from typing import Optional


class HarvestCreate(BaseModel):
    crop_type: str
    category: str
    quantity: float
    price_per_kg: float
    description: Optional[str] = None
