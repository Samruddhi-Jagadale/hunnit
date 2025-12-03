from sqlalchemy import Column, Integer, String, Numeric, JSON, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import LargeBinary
from sqlalchemy import Index
from sqlalchemy import text
from sqlalchemy_utils import TSVectorType
from sqlalchemy import func as safunc
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import Boolean

from .db import Base
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR

# If using pgvector, install and configure pgvector extension on DB. Here we keep embedding as JSON (fallback)
from sqlalchemy import Float

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=True)
    title = Column(String, nullable=False)
    price = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    features = Column(JSON, nullable=True)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    embedding = Column(JSON, nullable=True)  # If pgvector available, replace with vector column
    created_at = Column(TIMESTAMP, server_default=func.now())
