from pydantic import BaseModel, EmailStr


class SendCodeRequest(BaseModel):
    email: EmailStr


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str


class LogoutRequest(BaseModel):
    token: str


class SendCodeResponse(BaseModel):
    message: str


class VerifyCodeResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int


class LogoutResponse(BaseModel):
    message: str
