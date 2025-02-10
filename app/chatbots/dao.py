from app.dao.base import BaseDAO
from app.chatbots.models import Chatbot, Prompt


class ChatbotsDAO(BaseDAO):
    model = Chatbot


class PromptsDAO(BaseDAO):
    model = Prompt
