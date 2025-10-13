
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..models import Lead
from sqlmodel import Session, create_engine
import os
from typing import List

api_router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=False, future=True)

@api_router.get("/leads", response_model=List[Lead])
def list_leads():
    with Session(engine) as session:
        leads = session.exec(select(Lead).order_by(Lead.created_at.desc())).all()
        return leads

@api_router.post("/leads", response_model=Lead)
def create_lead(lead: Lead):
    with Session(engine) as session:
        session.add(lead)
        session.commit()
        session.refresh(lead)
        return lead
