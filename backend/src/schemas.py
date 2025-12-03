from pydantic import BaseModel
from typing import Optional, List, Any

class ProductCreate(BaseModel):
    sku: Optional[str]
    title: str
    price: Optional[str]
    currency: Optional[str]
    description: Optional[str]
    features: Optional[List[str]]
    category: Optional[str]
    image_url: Optional[str]
    source_url: Optional[str]
    metadata: Optional[dict]

class ProductOut(ProductCreate):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = []
