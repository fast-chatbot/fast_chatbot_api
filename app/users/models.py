from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, func
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now())

    # whatsapp_instance = relationship("WhatsAppInstance", back_populates="user")
    chatbot = relationship("Chatbot", back_populates="user")
