import sys
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
# Fix Psycopg 3 compatibility with asyncio on Windows
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routers import chat
from contextlib import asynccontextmanager
from app.graph.graph import build_support_graph
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.creds import credentials

# compiled_graph = None
# pool = None

@asynccontextmanager
async def lifespan(app:FastAPI):
    
    print("------Application Started -------")
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    pool = AsyncConnectionPool(conninfo=credentials.pg_db_uri, max_size=20, open=False, kwargs={"autocommit": True})
    await pool.open()

    checkpointer = AsyncPostgresSaver(conn=pool)

    await checkpointer.setup()

    app.state.graph = build_support_graph(checkpointer= checkpointer)
    print("------Application Startup Completed -------")
    yield

    await pool.close()


app = FastAPI(
    lifespan=lifespan,
    title="Customer Support Agent",
    version="0.1.1"
    )


@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse('/docs')

app.include_router(chat.route)