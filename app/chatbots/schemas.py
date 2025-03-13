from datetime import datetime

from pydantic import BaseModel


class AllChatbotsResponse(BaseModel):
    id: int
    user_id: int
    name: str
    model: str
    ai_tokens_limit: int
    created_at: datetime
    updated_at: datetime


class CreateRequest(BaseModel):
    name: str


class CreateResponse(BaseModel):
    message: str
    chatbot_id: int


class UpdateRequest(BaseModel):
    chatbot_id: int
    name: str


class UpdateResponse(BaseModel):
    message: str


class DeleteRequest(BaseModel):
    chatbot_id: int


class DeleteResponse(BaseModel):
    message: str


class AllPromptsResponse(BaseModel):
    id: int
    chatbot_id: int
    name: str
    text: str
    prompt_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AddPromptRequest(BaseModel):
    chatbot_id: int
    name: str
    text: str
    prompt_type: str
    is_active: bool

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


class DeletePromptRequest(BaseModel):
    prompt_id: int


class DeletePromptResponse(BaseModel):
    message: str
