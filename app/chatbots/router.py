from fastapi import APIRouter, HTTPException, status, Depends

from app.chatbots.dao import ChatbotsDAO, PromptsDAO
from app.chatbots.schemas import (AllResponse, CreateRequest, CreateResponse, UpdateRequest, UpdateResponse,
                                  DeleteRequest, DeleteResponse, UpdatePromptRequest, UpdatePromptResponse)
from app.users.models import User
from app.users.dependencies import get_current_user

from app.config import get_settings


settings = get_settings()

router = APIRouter(prefix='/chatbot', tags=['Chatbot'])


@router.get("/all", response_model=list[AllResponse])
async def get_chatbots():
    try:
        return await ChatbotsDAO.find_all(user_id=1)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error receiving the chatbots")


@router.post("/create", response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def chatbot_create(data: CreateRequest):
    try:
        chatbot = await ChatbotsDAO.add(
            user_id=1,
            name=data.name,
            model=data.model
        )

        return {"message": "Chatbot created successfully", "chatbot_id": chatbot.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create chatbot")


@router.post("/update", response_model=UpdateResponse)
async def chatbot_update(data: UpdateRequest, user_data: User = Depends(get_current_user)):
    try:
        await ChatbotsDAO.update(
            filter_by={'id': data.chatbot_id},
            name=data.name,
            model=data.model
        )

        return {"message": "Chatbot updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to update chatbot")


@router.post("/delete", response_model=DeleteResponse)
async def chatbot_delete(data: DeleteRequest, user_data: User = Depends(get_current_user)):
    try:
        await PromptsDAO.delete(delete_all=True, chatbot_id=data.chatbot_id)
        await ChatbotsDAO.delete(delete_all=True, id=data.chatbot_id)

        return {"message": "Chatbot deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to delete chatbot")


@router.get("/prompts", response_model=AllResponse)
async def get_prompts(data, user_data: User = Depends(get_current_user)):
    try:
        return await PromptsDAO.find_all(chatbot_id=data.chatbot_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error receiving the prompts")


@router.post("/add_prompt", response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def prompt_create(data: CreateRequest, user_data: User = Depends(get_current_user)):
    try:
        prompt = await PromptsDAO.add(
            chatbot_id=data.chatbot_id,
            name=data.name,
            text=data.text,
            prompt_type=data.prompt_type
        )

        return {"message": "Prompt created successfully", "prompt_id": prompt.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create prompt")


@router.post("/update_prompt", response_model=UpdatePromptResponse)
async def prompt_update(data: UpdatePromptRequest, user_data: User = Depends(get_current_user)):
    try:
        await PromptsDAO.update(
            filter_by={'id': data.promt_id},
            name=data.name,
            text=data.text,
            is_active=data.is_active
        )

        return {"message": "Prompt updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to update prompt")


