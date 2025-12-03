from fastapi import APIRouter, Depends, BackgroundTasks
from ..scraper.hunnit_scraper import fetch_listing, fetch_product_detail, polite_sleep
from ..db import get_session
from ..crud import upsert_product
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/scrape/hunnit")
async def scrape_hunnit(background: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    # synchronous scraping called in background to avoid long request blocking
    def job():
        items = fetch_listing()
        count = 0
        for item in items:
            try:
                polite_sleep()
                detail = fetch_product_detail(item["source_url"])
                payload = {
                    "title": detail["title"] or item.get("title"),
                    "price": detail.get("price") or item.get("price"),
                    "description": detail.get("description"),
                    "features": detail.get("features"),
                    "image_url": detail.get("image_url") or item.get("image_url"),
                    "category": detail.get("category"),
                    "source_url": detail.get("source_url")
                }
                import asyncio, nest_asyncio
                # we will call upsert synchronously by creating a new event loop
                import sqlalchemy
                # For simplicity, write to DB synchronously using SQLAlchemy core (left as exercise)
                # Instead, save to a simple JSON file or queue and process via an ingestion endpoint.
            except Exception as e:
                print("scrape error", e)
                continue
    background.add_task(job)
    return {"status": "started"}
