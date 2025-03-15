from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Query, Depends

from app.users.models import User
from app.users.dependencies import get_current_user
from app.chat_with_chatbot.dao import UserChatbotTestMessageDAO
from app.gpt_chatbot import GptChatBot
from app.config import get_settings
from app.chat_with_chatbot.schemas import UserChatbotTestMessagesResponse


router = APIRouter(tags=['Chat with chatbot'])


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket:dict] = {}

    async def connect(self, websocket: WebSocket, user_id: int, chatbot_id: int):
        await websocket.accept()

        self.active_connections[websocket] = {
            'user_id': user_id,
            'chatbot_id': chatbot_id,
        }

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             token: str = Query(None),
                             chatbot_id: int = Query(..., description="ID чатбота")):
    user_data: User = await get_current_user(token)

    await manager.connect(websocket, user_data.id, chatbot_id)

    try:
        while True:
            data = await websocket.receive_text()

            await save_message(text=data,
                               user_id=user_data.id,
                               chatbot_id=chatbot_id,
                               sender='user')

            last_messages_raw = await UserChatbotTestMessageDAO().get_last_messages(user_id=user_data.id,
                                                                                    chatbot_id=chatbot_id)

            last_messages: list[dict] =[]

            for message in last_messages_raw.__reversed__():
                last_messages.append({
                    'role': message['sender'],
                    'content': message['text']
                })

            chatbot = GptChatBot(api_key=get_settings()['openai_api_key'])
            answer = await chatbot.ask(last_messages=last_messages, chatbot_id=chatbot_id)

            if answer:
                await save_message(text=answer,
                                   user_id=user_data.id,
                                   chatbot_id=chatbot_id,
                                   sender='system')

                await websocket.send_text(answer)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def save_message(text: str, user_id: int, chatbot_id: int, sender: str):
    await UserChatbotTestMessageDAO.add(text=text,
                                        user_id=user_id,
                                        chatbot_id=chatbot_id,
                                        sender=sender)

@router.get("/chatbot/user-test-messages", response_model=list[UserChatbotTestMessagesResponse])
async def get_messages(chatbot_id: int = Query(..., description="ID чатбота"),
                       user_data: User = Depends(get_current_user)):
    messages = await UserChatbotTestMessageDAO.get_messages(user_id=user_data.id, chatbot_id=chatbot_id)

    return messages
