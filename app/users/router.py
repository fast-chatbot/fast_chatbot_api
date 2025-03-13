import redis.asyncio as redis

from fastapi import APIRouter, HTTPException, Depends

from app.users.auth import create_access_token, generate_otp, send_email
from app.users.models import User
from app.users.dao import UsersDAO
from app.users.schemas import (SendCodeRequest, VerifyCodeRequest, LogoutRequest, SendCodeResponse, VerifyCodeResponse,
                               LogoutResponse)
from app.users.dependencies import get_current_user

from datetime import timedelta
from app.config import get_settings


settings = get_settings()

router = APIRouter(prefix='/auth', tags=['Auth'])
redis_client = redis.StrictRedis(host=settings['redis_host'],
                                 port=settings['redis_port'],
                                 db=0,
                                 password=settings['redis_password'],
                                 decode_responses=True)
TOKEN_TTL = 3600


@router.post("/send-code", response_model=SendCodeResponse)
async def send_code(data: SendCodeRequest):
    try:
        otp = generate_otp()
        await redis_client.setex(f"fast_chatbot_online_otp:{data.email}", 900, otp)

        print(data.email)
        print(otp)
        # send_email(data.email, otp)

        return {"message": "OTP sent successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error sending the OTP-code")


@router.post("/verify-code", response_model=VerifyCodeResponse)
async def verify_code(data: VerifyCodeRequest):
    try:
        stored_otp = await redis_client.get(f"fast_chatbot_online_otp:{data.email}")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Internal server error")

    if not stored_otp or stored_otp != data.code:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    try:
        await redis_client.delete(f"otp:{data.email}")

        user: User
        user = await UsersDAO.find_one_or_none(email=data.email)

        if not user:
            user = await UsersDAO.add(
                email=data.email,
            )

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(days=365)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Internal server error")

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@router.post("/logout", response_model=LogoutResponse)
async def logout(data: LogoutRequest, user_data: User = Depends(get_current_user)):
    try:
        await redis_client.setex(data.token, TOKEN_TTL, "blacklisted")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Logout error")

    return {"message": "Logout successful"}




