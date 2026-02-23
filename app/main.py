from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import require_api_key
from .db import Base, engine, SessionLocal
from .models import Ticket
from .schemas import TicketCreate, TicketPatch, TicketOut
from fastapi import BackgroundTasks
from .ticket_ai import analyze_ticket

# Create tables on startup (simple for local dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Ticket Automation API", version="0.1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def process_ticket_in_background(ticket_id: int):
    """
    Runs in background:
    - loads the ticket from DB
    - calls OpenAI via LangChain
    - updates ticket with AI output
    """
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return

        # If already processed, skip
        if ticket.status != "NEW":
            return

        ai = analyze_ticket(title=ticket.title, description=ticket.description)

        ticket.ai_summary = ai["summary"]
        ticket.ai_priority = ai["priority"]
        ticket.ai_draft_reply = ai["draft_reply"]
        ticket.status = "PROCESSED"

        db.commit()

    except Exception:
        # If anything fails, mark as ERROR (useful for debugging)
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket:
            ticket.status = "ERROR"
            db.commit()
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}


# @app.post("/tickets", response_model=TicketOut)
# def create_ticket(payload: TicketCreate, db: Session = Depends(get_db), _: bool = Depends(require_api_key)):
#     ticket = Ticket(
#         title=payload.title,
#         description=payload.description,
#         status="NEW",
#     )
#     db.add(ticket)
#     db.commit()
#     db.refresh(ticket)
#     return ticket

@app.post("/tickets", response_model=TicketOut)
def create_ticket(
    payload: TicketCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: bool = Depends(require_api_key),
):
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        status="NEW",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Trigger AI processing immediately (no scheduler needed)
    background_tasks.add_task(process_ticket_in_background, ticket.id)

    return ticket


@app.get("/tickets", response_model=List[TicketOut])
def list_tickets(status: Optional[str] = None, db: Session = Depends(get_db), _: bool = Depends(require_api_key)):
    q = db.query(Ticket)
    if status:
        q = q.filter(Ticket.status == status)
    return q.order_by(Ticket.id.desc()).all()


@app.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), _: bool = Depends(require_api_key)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.patch("/tickets/{ticket_id}", response_model=TicketOut)
def patch_ticket(ticket_id: int, payload: TicketPatch, db: Session = Depends(get_db), _: bool = Depends(require_api_key)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    updates = payload.model_dump(exclude_unset=True)

    # Apply updates only for provided fields
    for field, value in updates.items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return ticket