from fastapi import APIRouter, Depends, HTTPException
from ..schemas import ChatRequest
from ..db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..embeddings import make_embedding
from ..rag import retrieve_candidates, format_prompt, generate_answer_openai
import json

router = APIRouter()

@router.post("/chat")
async def chat(req: ChatRequest, session: AsyncSession = Depends(get_session)):
    q = req.query
    q_emb = make_embedding(q)
    candidates = await retrieve_candidates(session, q_emb, limit=8)
    prompt = format_prompt(q, candidates)
    # If user has OPENAI_API_KEY, use OpenAI; else return deterministic shortlist
    try:
        answer = generate_answer_openai(prompt)
    except Exception as e:
        # fallback: return top 3 candidates with template reasons
        recs = []
        for p in candidates[:3]:
            reason = f"Matches because of features: {', '.join(p.get('features') or [])[:120]}"
            recs.append({"id": p["id"], "title": p["title"], "reason": reason, "image_url": p.get("image_url"), "source_url": p.get("source_url")})
        return {"message": "fallback results", "recommendations": recs}
    # try to parse JSON from LLM or return raw
    try:
        parsed = json.loads(answer)
    except:
        parsed = {"message": answer}
    return parsed
