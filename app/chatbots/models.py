from sqlalchemy import (
    Column, Integer, ForeignKey, TIMESTAMP, func, String, Boolean
)
from sqlalchemy.orm import relationship

from app.database import Base


class Chatbot(Base):
    __tablename__ = 'chatbots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False, default='chatgpt')
    ai_tokens_limit = Column(Integer, nullable=False, default=2000)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now())

    user = relationship("User", back_populates="chatbot")


class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chatbot_id = Column(Integer, ForeignKey('chatbots.id'), nullable=False)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    prompt_type = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now())

