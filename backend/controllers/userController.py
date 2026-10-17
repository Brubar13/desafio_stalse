from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import (HTTPBearer, OAuth2PasswordBearer)
from sqlalchemy.orm import Session
from sqlalchemy import select

security = HTTPBearer()

#DATABASE
from db.database import get_db
from infra.providers import encrypt_provider, token_provider
from models.user import User

from Schemas.Schemas import (
    CreateUserRequest,
    UsersResponse,
    PatchUserRequest
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
def get_all_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user = db.scalar(statement)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )

    statement = select(User)
    users = db.scalars(statement).all()

    return users

@router.patch("/{user_id}", response_model=UsersResponse)
def atualiza_usuario(user_id: int, dados_atualizados: PatchUserRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user_loged = db.scalar(statement)

    user_update = db.get(User, user_id)

    if (
        not user_loged or 
        (user_loged.role != "admin" and 
        user_loged.id != user_update.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
        )

    if (user_loged.role != "admin" and (dados_atualizados.is_active != None or dados_atualizados.role != None)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Somente admins podem alterar a Role ou a Validade de um usuario... Contate o admin",
        )
    
    print(dados_atualizados)
    if dados_atualizados.name is not None:
        user_update.name = dados_atualizados.name

    if dados_atualizados.email is not None:
        user_update.email = dados_atualizados.email

    if dados_atualizados.password is not None:
        print("Caiu na atualização de senha!")
        user_update.password_hash = encrypt_provider.hash_password(dados_atualizados.password)

    if dados_atualizados.role is not None and user_loged.role == 'admin':
        user_update.role = dados_atualizados.role

    if dados_atualizados.is_active is not None and user_loged.role == 'admin':
        user_update.is_active = dados_atualizados.is_active 

    db.commit()
    db.refresh(user_update)
    
    return user_update

@router.get("/{user_id}", response_model=UsersResponse)
def atualiza_status_priority_ticket(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validateHeader = token_provider.validateAcessToken(token)
    
    statement = select(User).where(User.email == validateHeader)
    user_loged = db.scalar(statement)

    if not user_loged or (user_loged.role != "admin" and user_loged.id != user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario Invalido",
    )

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario não encontrado",
        )
    
    return user