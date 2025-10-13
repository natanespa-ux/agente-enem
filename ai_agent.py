
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os
import openai

api_router = APIRouter()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

@api_router.get("/ai-response")
async def ai_response(prompt: str = Query(...)):
    if not OPENAI_KEY:
        return JSONResponse(status_code=501, content={"error":"OpenAI key not configured"})
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system","content":"Você é o Atendente ENEM, objetivo: vender o manual com linguagem direta e educada."},
                      {"role":"user","content":prompt}],
            max_tokens=500
        )
        answer = resp["choices"][0]["message"]["content"]
        return JSONResponse(status_code=200, content={"answer": answer})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
