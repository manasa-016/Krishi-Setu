from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Harvest(Base):
    __tablename__ = "harvests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    crop_type = Column(String, nullable=False)
    category = Column(String, nullable=False)  # vegetables/fruits/flowers
    quantity = Column(Float, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
