from sqlalchemy import (
    Column, Integer, ForeignKey, TIMESTAMP, func, String, Enum
)

from app.database import Base


class UserChatbotTestMessage(Base):
    __tablename__ = 'user_chatbot_test_messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chatbot_id = Column(Integer, ForeignKey('chatbots.id'), nullable=False)
    sender = Column(Enum('user', 'system', name='sender_role'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
