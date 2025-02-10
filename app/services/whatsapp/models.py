from sqlalchemy import (
    Column, Integer, ForeignKey, TIMESTAMP, func, String, Boolean
)
from sqlalchemy.orm import relationship

from app.database import Base


class WhatsAppInstance(Base):
    __tablename__ = 'whatsapp_instances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone_number = Column(String, nullable=False)
    is_auth = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    expires_on = Column(TIMESTAMP, nullable=False, default=func.now())
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now())

    user = relationship("User", back_populates="whatsapp_instance")
