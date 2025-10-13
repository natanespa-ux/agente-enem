
import os
import httpx

ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

async def send_text(phone: str, message: str):
    if not ZAPI_INSTANCE or not ZAPI_TOKEN:
        raise RuntimeError("Z-API credentials not set")
    # Using common Z-API REST format; adjust endpoint if your plan differs
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    payload = {"phone": phone, "message": message}
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
