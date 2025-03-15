from app.dao.base import BaseDAO
from app.chatbots.models import Chatbot, Prompt
from app.database import async_session_maker

from sqlalchemy.future import select


class ChatbotsDAO(BaseDAO):
    model = Chatbot


class PromptsDAO(BaseDAO):
    model = Prompt

    @staticmethod
    async def get_prompts(chatbot_id: int) -> list[str]:
        async with async_session_maker() as session:
            query = select(Prompt.text).filter_by(chatbot_id=chatbot_id).order_by(Prompt.id.asc())
            result = await session.execute(query)

            return result.scalars().all()

# async def main():
#     dao = PromptsDAO()
#     data = await dao.get_prompts(1)
#     print(data)
#
# asyncio.run(main())
