from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordBearer)
from jose import JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select

security = HTTPBearer()

#DATABASE
from db.database import get_db
from infra.providers import encrypt_provider, token_provider
from models.user import User

from Schemas.Schemas import (
    CreateUserRequest,
    UsersResponse
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/create")
def create_user(create_user: CreateUserRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )

    new_user = User(
        name=create_user.name,
        email=create_user.email,
        password_hash=encrypt_provider.hash_password(create_user.password),
        role=create_user.role,
        is_active=True,
     
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(content={"message": "Usuario criado com sucesso"})

@router.get("/all_users", response_model=list[UsersResponse])
def get_all_tickets(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )

    statement = select(User)
    tickets = db.scalars(statement).all()


    return tickets