from sentence_transformers import SentenceTransformer
import numpy as np
from .config import settings

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def make_embedding(text):
    model = get_model()
    emb = model.encode([text])[0]  # numpy array
    return emb.astype(float).tolist()
