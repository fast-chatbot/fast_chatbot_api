from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

from app.config import get_settings


settings = get_settings()

pg_host = settings['pg_host']
pg_port = settings['pg_port']
pg_user = settings['pg_user']
pg_password = settings['pg_password']
pg_database = settings['pg_database']

database_url = f'postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


