from fastapi import FastAPI
from .routers import products, scrape, chat
from .db import engine, Base
import asyncio

app = FastAPI(title="Hunnit Product Discovery - Backend")

app.include_router(products.router, prefix="/api")
app.include_router(scrape.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.on_event("startup")
async def startup():
    # create tables (for dev)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
