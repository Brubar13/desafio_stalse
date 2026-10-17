from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (HTTPBearer, OAuth2PasswordBearer)
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

security = HTTPBearer()

#DATABASE
from db.database import get_db
from infra.providers import token_provider
from models.user import User
from models.customer import Customer

#SCHEMAS
from Schemas.Schemas import ( 
    CreateCustomerRequest,
    CustomerResponse,
    PatchCustomerRequest
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/create", response_model=CustomerResponse)
def create_new_customer(customer_to_create: CreateCustomerRequest,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

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
    
    new_customer = Customer(
        name= customer_to_create.name,
        email= customer_to_create.email,
        phone= customer_to_create.phone
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return new_customer

@router.get("/{customer_id}", response_model=CustomerResponse)
def atualiza_status_priority_ticket(customer_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
    )

    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer não encontrado",
        )
    
    return customer

@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )

    

    statement = select(Customer)
    customers = db.scalars(statement).all()


    return customers

@router.patch("/{customer_id}", response_model=CustomerResponse)
def atualiza_customer(customer_id: int, dados_atualizados: PatchCustomerRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user_loged = db.scalar(statement)

    customer_update = db.get(Customer, customer_id)

    if (
        not user_loged or 
        user_loged.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )
    
    if dados_atualizados.name is not None:
        customer_update.name = dados_atualizados.name

    if dados_atualizados.email is not None:
        customer_update.email = dados_atualizados.email

    if dados_atualizados.phone is not None:
        customer_update.phone = dados_atualizados.phone
   
    customer_update.updated_at = datetime.now() 

    db.commit()
    db.refresh(customer_update)
    
    return customer_update