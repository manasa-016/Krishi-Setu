from sqlalchemy import Column, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

# This imports Base as it would be resolved when merged into the main Agritech-b repo
from app.core.database import Base

class UserLocation(Base):
    __tablename__ = "user_locations"

    # We use UUID to match the main repo's ID format
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 1-to-1 relationship with the users table. Unique ensures a user has only one location record.
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
