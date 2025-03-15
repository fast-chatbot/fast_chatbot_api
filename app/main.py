from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import TokenExpiredException, TokenNoFoundException

from app.users.router import router as auth_router
from app.chatbots.router import router as chatbots_router
from app.chat_with_chatbot.router import router as chat_with_chatbot_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(auth_router)
app.include_router(chatbots_router)
app.include_router(chat_with_chatbot_router)


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    pass


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    pass

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print(11)


