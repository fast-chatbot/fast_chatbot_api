from fastapi import APIRouter, HTTPException, status, Depends, Query

from app.chatbots.dao import ChatbotsDAO, PromptsDAO
from app.chatbots.schemas import (AllChatbotsResponse, CreateRequest, CreateResponse, UpdateRequest, UpdateResponse,
                                  DeleteRequest, DeleteResponse, AllPromptsResponse, UpdatePromptRequest,
                                  UpdatePromptResponse, AddPromptRequest, AddPromptResponse, DeletePromptRequest,
                                  DeletePromptResponse)
from app.users.models import User
from app.users.dependencies import get_current_user

from app.config import get_settings


settings = get_settings()

router = APIRouter(prefix='/chatbot', tags=['Chatbot'])


# @router.get("/test")
# async def get_chatbots1():
#     data = await GptChatBot('d').ask('')
#     print(data)

@router.get("/all", response_model=list[AllChatbotsResponse])
async def get_chatbots(user_data: User = Depends(get_current_user)):
    try:
        return await ChatbotsDAO.find_all(user_id=user_data.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error receiving the chatbots")


@router.post("/create", response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
async def chatbot_create(data: CreateRequest, user_data: User = Depends(get_current_user)):
    try:
        chatbot = await ChatbotsDAO.add(
            user_id=user_data.id,
            name=data.name
        )

        return {"message": "Chatbot created successfully", "chatbot_id": chatbot.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create chatbot")


@router.post("/update", response_model=UpdateResponse)
async def chatbot_update(data: UpdateRequest, user_data: User = Depends(get_current_user)):
    try:
        await ChatbotsDAO.update(
            filter_by={'id': data.chatbot_id, 'user_id': user_data.id},
            name=data.name
        )

        return {"message": "Chatbot updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to update chatbot")


@router.post("/delete", response_model=DeleteResponse)
async def chatbot_delete(data: DeleteRequest, user_data: User = Depends(get_current_user)):
    try:
        chatbot_data = await ChatbotsDAO.find_one_or_none(id=data.chatbot_id)

        if chatbot_data.user_id == user_data.id:
            await PromptsDAO.delete(delete_all=True, chatbot_id=data.chatbot_id)
            await ChatbotsDAO.delete(delete_all=True, id=data.chatbot_id)
        else:
            raise HTTPException(status_code=404, detail="Chatbot not found")

        return {"message": "Chatbot deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to delete chatbot")


@router.get("/prompts", response_model=list[AllPromptsResponse])
async def get_prompts(chatbot_id: int = Query(..., description="ID чатбота"), user_data: User = Depends(get_current_user)):
    try:
        chatbot_data = await ChatbotsDAO.find_one_or_none(id=chatbot_id)

        if chatbot_data.user_id == user_data.id:
            return await PromptsDAO.find_all(chatbot_id=chatbot_id)
        else:
            raise HTTPException(status_code=404, detail="Chatbot not found")

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error receiving the prompts")


@router.post("/add_prompt", response_model=AddPromptResponse, status_code=status.HTTP_201_CREATED)
async def prompt_create(data: AddPromptRequest, user_data: User = Depends(get_current_user)):
    try:
        chatbot_data = await ChatbotsDAO.find_one_or_none(id=data.chatbot_id)

        if chatbot_data.user_id == user_data.id:
            prompt = await PromptsDAO.add(
                chatbot_id=data.chatbot_id,
                name=data.name,
                text=data.text,
                prompt_type=data.prompt_type
            )
        else:
            raise HTTPException(status_code=404, detail="Chatbot not found")

        return {"message": "Prompt created successfully", "prompt_id": prompt.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create prompt")


@router.post("/update_prompt", response_model=UpdatePromptResponse)
async def prompt_update(data: UpdatePromptRequest, user_data: User = Depends(get_current_user)):
    # try:
    prompt_data = await PromptsDAO.find_one_or_none(id=data.prompt_id)
    chatbot_data = await ChatbotsDAO.find_one_or_none(id=prompt_data.chatbot_id)

    if chatbot_data.user_id == user_data.id:
        await PromptsDAO.update(
            filter_by={'id': data.prompt_id},
            name=data.name,
            text=data.text,
            is_active=data.is_active
        )
    else:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return {"message": "Prompt updated successfully"}
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail="Failed to update prompt")


@router.post("/delete_prompt", response_model=DeletePromptResponse)
async def prompt_delete(data: DeletePromptRequest, user_data: User = Depends(get_current_user)):
    try:
        prompt_data = await PromptsDAO.find_one_or_none(id=data.prompt_id)
        chatbot_data = await ChatbotsDAO.find_one_or_none(id=prompt_data.chatbot_id)

        if chatbot_data.user_id == user_data.id:
            await PromptsDAO.delete(delete_all=True, id=data.prompt_id)
        else:
            raise HTTPException(status_code=404, detail="Prompt not found")

        return {"message": "Prompt deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to update prompt")

