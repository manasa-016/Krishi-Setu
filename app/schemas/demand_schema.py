from pydantic import BaseModel


class DemandCreate(BaseModel):
    crop_type: str
    category: str
    required_quantity: float
    offered_price: float
