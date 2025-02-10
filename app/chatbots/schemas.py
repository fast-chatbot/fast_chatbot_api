from datetime import datetime

from pydantic import BaseModel


class AllResponse(BaseModel):
    id: int
    user_id: int
    name: str
    model: str
    ai_tokens_limit: int
    created_at: datetime
    updated_at: datetime


class CreateRequest(BaseModel):
    name: str
    model: str


class CreateResponse(BaseModel):
    message: str
    chatbot_id: int


class UpdateRequest(BaseModel):
    chatbot_id: int
    name: str
    model: str


class UpdateResponse(BaseModel):
    message: str


class DeleteRequest(BaseModel):
    chatbot_id: int


class DeleteResponse(BaseModel):
    message: str


class AddPromptRequest(BaseModel):
    chatbot_id: int
    text: str
    prompt_type: str


class AddPromptResponse(BaseModel):
    message: str
    prompt_id: int


class UpdatePromptRequest(BaseModel):
    prompt_id: int
    name: str
    text: str
    is_active: bool


class UpdatePromptResponse(BaseModel):
    message: str
