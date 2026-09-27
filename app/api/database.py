from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import declarative_base, sessionmaker
from ..creds import credentials

engine = create_async_engine(
        f"mysql+aiomysql://{credentials.db_username}:{credentials.db_password}@{credentials.db_host}:{credentials.db_port}/{credentials.db_schema}",
        echo=False,
    )
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            

Base = declarative_base()