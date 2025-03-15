from app.dao.base import BaseDAO
from app.chat_with_chatbot.models import UserChatbotTestMessage
from app.database import async_session_maker

from sqlalchemy.future import select


class UserChatbotTestMessageDAO(BaseDAO):
    model = UserChatbotTestMessage

    @staticmethod
    async def get_last_messages(user_id: int, chatbot_id: int, limit: int = 10):
        async with async_session_maker() as session:
            query = select(
                UserChatbotTestMessage.sender,
                UserChatbotTestMessage.text
            ).filter_by(
                user_id=user_id,
                chatbot_id=chatbot_id
            ).order_by(
                UserChatbotTestMessage.created_at.desc()
            ).limit(limit)

            result = await session.execute(query)

            return [dict(row._asdict()) for row in result.all()]

    @staticmethod
    async def get_messages(user_id: int, chatbot_id: int):
        async with async_session_maker() as session:
            query = select(
                UserChatbotTestMessage
            ).filter_by(
                user_id=user_id,
                chatbot_id=chatbot_id
            ).order_by(
                UserChatbotTestMessage.created_at.asc()
            )

            result = await session.execute(query)

            return result.scalars().all()
