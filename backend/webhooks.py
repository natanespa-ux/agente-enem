
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os, logging, httpx
from ...services.zapi import send_text
from ...models import Lead
from sqlmodel import Session, create_engine, select

api_router = APIRouter()
logger = logging.getLogger("webhooks")
logger.setLevel(logging.INFO)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=False, future=True)

WELCOME_TEXT = (
    "Olá! 👋 Eu sou o Representante ENEM.\n"
    "Antes de começarmos, salve meu contato como *Representante ENEM* para receber o material completo.\n"
    "Digite SAIR a qualquer momento se não quiser continuar."
)

EXIT_KEYWORDS = ["sair", "remover", "cancelar", "parar"]

@api_router.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()
        message = (data.get("message", {}).get("text") or data.get("body") or "").strip().lower()
        phone = data.get("message", {}).get("from") or data.get("from") or data.get("phone") or ""
        logger.info(f"Received from {phone}: {message}")

        # ensure lead exists
        with Session(engine) as session:
            stmt = select(Lead).where(Lead.phone == phone)
            lead = session.exec(stmt).first()
            if not lead:
                # create minimal lead
                new = Lead(phone=phone)
                session.add(new); session.commit()
                lead = new

        # handle opt-out
        if any(k in message for k in EXIT_KEYWORDS):
            with Session(engine) as session:
                stmt = select(Lead).where(Lead.phone == phone)
                lead = session.exec(stmt).first()
                if lead:
                    lead.is_active = False
                    session.add(lead); session.commit()
            try:
                await send_text(phone, "Tudo certo 👋 Você foi removido da nossa lista. Caso queira voltar, é só enviar 'voltar'.")
            except Exception as e:
                logger.error("Failed optout send: %s", e)
            return JSONResponse(status_code=200, content={"action":"lead_removed"})

        # greeting
        if message in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]:
            try:
                await send_text(phone, WELCOME_TEXT)
            except Exception as e:
                logger.error("Failed to send welcome: %s", e)
            return JSONResponse(status_code=200, content={"action":"welcome_sent"})

        # voltar handling
        if "voltar" in message:
            try:
                await send_text(phone, "Bem-vindo de volta! 😊 Para garantir que receba tudo certinho, salve meu contato como Representante ENEM.")
            except Exception as e:
                logger.error("Failed to send voltar: %s", e)
            return JSONResponse(status_code=200, content={"action":"reactivated"})

        # simple CTA flow: if user says "sim" send payment link (placeholder)
        if "sim" in message:
            # send simulated checkout link - replace with real payment flow integration
            try:
                await send_text(phone, "Ótimo! Aqui está o link para pagamento via PIX: https://pagamento.exemplo/pagar?produto=manual-enem")
            except Exception as e:
                logger.error("Failed to send payment link: %s", e)
            return JSONResponse(status_code=200, content={"action":"sent_checkout"})

        # default fallback
        cta = ("Olá! Posso te enviar agora o *Manual do ENEM Definitivo* por um preço especial? "
               "Responda SIM para receber o link de pagamento.")
        try:
            await send_text(phone, cta)
        except Exception as e:
            logger.error("Failed to send CTA: %s", e)
        return JSONResponse(status_code=200, content={"action":"cta_sent"})

    except Exception as e:
        logger.error("Webhook error: %s", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
