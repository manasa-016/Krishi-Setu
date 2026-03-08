from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
