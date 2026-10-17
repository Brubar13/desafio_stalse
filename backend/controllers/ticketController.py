from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordBearer)
from datetime import datetime
from jose import JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select

security = HTTPBearer()

#DATABASE
from db.database import get_db
from infra.providers import token_provider
from models.user import User
from models.ticket import Ticket

#SCHEMAS
from Schemas.Schemas import (
    TicketResponse, 
    CreateTicketRequest,
    PatchTicketRequest
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.get("/", response_model=list[TicketResponse])
def get_all_tickets(
    customer_id: int | None = None,
    assigned_user_id: int | None = None,
    status: str | None = None,
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )

    filters = []

    if customer_id is not None:
        filters.append(Ticket.customer_id == customer_id)

    if assigned_user_id is not None:
        filters.append(Ticket.assigned_user_id == assigned_user_id)

    if status is not None:
        filters.append(Ticket.status == status)

    statement = select(Ticket).where(*filters)
    tickets = db.scalars(statement).all()


    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
def atualiza_status_priority_ticket(ticket_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
    )

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado",
        )
    
    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
def atualiza_status_priority_ticket(ticket_id: int, dados_atualizados: PatchTicketRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado",
        )

    if (
        not user or 
        user.role != "admin" and 
        user.id != ticket.assigned_user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )
    
    if (
        dados_atualizados.priority == None and dados_atualizados.status == None
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Preencha atualização de status ou prioridade... Os dois não podem estar Null",
        )

    if dados_atualizados.status is not None:
        ticket.status = dados_atualizados.status

    if dados_atualizados.priority is not None:
        ticket.priority = dados_atualizados.priority

    ticket.updated_at = datetime.now()    

    db.commit()
    db.refresh(ticket)
    
    return ticket

@router.post("/create", response_model=TicketResponse)
def create_new_ticket(ticket_to_create: CreateTicketRequest,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if (
        not user or 
        user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
    )

    new_ticket = Ticket(
        subject= ticket_to_create.subject,
        channel= ticket_to_create.channel,
        status= ticket_to_create.status,
        priority= ticket_to_create.priority,
        assigned_user_id= ticket_to_create.assigned_user_id if ticket_to_create.assigned_user_id != None else None,
        customer_id= ticket_to_create.customer_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket