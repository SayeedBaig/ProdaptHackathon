import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID

class User(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    startups = relationship("Startup", back_populates="user", cascade="all, delete-orphan")
