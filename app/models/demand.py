from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Demand(Base):
    __tablename__ = "demands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    crop_type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    required_quantity = Column(Float, nullable=False)
    offered_price = Column(Float, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
