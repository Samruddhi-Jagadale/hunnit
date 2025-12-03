from sqlalchemy.future import select
from sqlalchemy import update
from .models import Product

async def upsert_product(session, product_dict):
    # upsert by source_url or sku
    q = await session.execute(select(Product).where(Product.source_url == product_dict.get("source_url")))
    instance = q.scalars().first()
    if instance:
        for k, v in product_dict.items():
            setattr(instance, k, v)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
    else:
        obj = Product(**product_dict)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

async def list_products(session, limit=20, offset=0):
    q = await session.execute(select(Product).limit(limit).offset(offset).order_by(Product.id))
    return q.scalars().all()

async def get_product(session, product_id):
    q = await session.execute(select(Product).where(Product.id == product_id))
    return q.scalars().first()
