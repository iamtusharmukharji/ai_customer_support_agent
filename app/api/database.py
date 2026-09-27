# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker
from ..creds import credentials

# async_engine = create_async_engine(
#         f"mysql+aiomysql://{credentials.db_username}:{credentials.db_password}@{credentials.db_host}:{credentials.db_port}/{credentials.db_schema}",
#         echo=False,
#     )

engine = create_engine(
        f"mysql+pymysql://{credentials.db_username}:{credentials.db_password}@{credentials.db_host}:{credentials.db_port}/{credentials.db_schema}",
        pool_size=10,         # Keeps up to 10 connections open
        max_overflow=20,     # Allows up to 20 temporary extra connections
        pool_recycle=3600, 
    )
# AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

SessionLocal = sessionmaker(engine, expire_on_commit=False )

async def get_db_async():
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db():
    
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
            

Base = declarative_base()