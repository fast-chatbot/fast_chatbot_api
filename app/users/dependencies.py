from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import get_settings
from app.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, TokenNoFoundException
from app.users.dao import UsersDAO


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        settings = get_settings()

        payload = jwt.decode(token, settings['secret_key'], algorithms=settings['algorithm'])
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')

    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user
