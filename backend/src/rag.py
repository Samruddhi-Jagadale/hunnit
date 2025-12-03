from .embeddings import make_embedding
import numpy as np
from sqlalchemy import text
from .config import settings
import json
import openai  # optional; used only if OPENAI_API_KEY provided

def build_canonical_text(product):
    features = product.get("features") or []
    return f"Title: {product.get('title')}\nPrice: {product.get('price')}\nCategory: {product.get('category')}\nFeatures: {', '.join(features)}\nDescription: {product.get('description') or ''}"

async def retrieve_candidates(session, query_emb, limit=8):
    """
    Simple retrieval: compute cosine similarity in Python for JSON embeddings column.
    If you have pgvector, push computation into DB for speed.
    """
    # naive: load all embeddings (works for small dataset)
    res = await session.execute(text("SELECT id, title, price, description, features, image_url, source_url, embedding FROM products"))
    rows = res.fetchall()
    cand = []
    q = np.array(query_emb, dtype=float)
    for row in rows:
        emb = row.embedding
        if not emb:
            continue
        e = np.array(emb, dtype=float)
        # cosine similarity:
        dot = float(np.dot(q, e))
        denom = float((np.linalg.norm(q) * np.linalg.norm(e)) + 1e-10)
        sim = dot/denom
        cand.append((sim, dict(id=row.id, title=row.title, price=row.price, description=row.description, features=row.features, image_url=row.image_url, source_url=row.source_url)))
    cand.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in cand[:limit]]

def format_prompt(user_query, candidates):
    prompt = "You are a helpful product discovery assistant. A user asked the following:\n\n"
    prompt += f"User Query: {user_query}\n\n"
    prompt += "You have these candidate products:\n"
    for i, p in enumerate(candidates, start=1):
        prompt += f"{i}) {p['title']} — Price: {p.get('price')} — Features: {', '.join(p.get('features') or [])}\n"
    prompt += "\nTask: Recommend up to 3 of the best products for the user, with 1-2 sentence reasons each. If the query is ambiguous, ask one brief clarifying question. Return JSON with keys: recommendations (list of {id, reason}), clarifying_question (optional).\n"
    return prompt

def generate_answer_openai(prompt):
    openai.api_key = settings.OPENAI_API_KEY
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"You are a product discovery assistant."},
                  {"role":"user","content":prompt}],
        max_tokens=400,
        temperature=0.3
    )
    return resp["choices"][0]["message"]["content"]
