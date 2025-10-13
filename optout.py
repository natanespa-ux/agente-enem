
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..models import Lead
from sqlmodel import Session, create_engine
import os

api_router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=False, future=True)

@api_router.post("/optout")
def optout_user(phone: str):
    with Session(engine) as session:
        stmt = select(Lead).where(Lead.phone == phone)
        lead = session.exec(stmt).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        lead.is_active = False
        session.add(lead)
        session.commit()
        return {"message": f"{phone} unsubscribed"}
