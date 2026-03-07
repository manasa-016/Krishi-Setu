from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    harvest_id = Column(UUID(as_uuid=True), ForeignKey("harvests.id"), nullable=False)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")  # pending/completed/cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
