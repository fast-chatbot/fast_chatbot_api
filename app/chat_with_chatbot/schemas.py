from datetime import datetime

from pydantic import BaseModel


class UserChatbotTestMessagesResponse(BaseModel):
    id: int
    text: str
    user_id: int
    chatbot_id: int
    sender: str
    created_at: datetime
