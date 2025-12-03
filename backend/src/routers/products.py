from fastapi import APIRouter, Depends, HTTPException, Query
from ..db import get_session
from ..crud import list_products, get_product
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import ProductOut

router = APIRouter()

@router.get("/products", response_model=list[ProductOut])
async def products(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), session: AsyncSession = Depends(get_session)):
    offset = (page-1)*limit
    items = await list_products(session, limit=limit, offset=offset)
    return items

@router.get("/products/{product_id}", response_model=ProductOut)
async def product_detail(product_id: int, session: AsyncSession = Depends(get_session)):
    item = await get_product(session, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
