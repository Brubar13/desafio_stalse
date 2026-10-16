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

#SCHEMAS
from Schemas.Schemas import LoginRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="refreshToken")

router = APIRouter()

@router.post("/login")
def login(loginData: LoginRequest, db: Session = Depends(get_db)):

    statement = select(User).where(User.email == loginData.email)
    user = db.scalar(statement)

    if (user is None or not encrypt_provider.verify_password(loginData.password, user.password_hash) or not user.is_active):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )

    tokens = token_provider.createAcessToken({ 'sub': user.email })

    return JSONResponse(content={"tokens": tokens, "nome": user.name, "email": user.email, "profileType": user.role })

@router.post("/refreshToken")
async def refresh_token_endpoint(request: Request):
    try:
        body = await request.json()
        refresh_token = body.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token não fornecido")

        email = token_provider.validateAcessToken(refresh_token)

        if not email:
            raise HTTPException(status_code=401, detail="Refresh token inválido")

        new_tokens = token_provider.createAcessToken({"sub": email})

        return {"tokens": new_tokens}

    except JWTError as e:
        print("Erro na validação do token:", e)
        raise HTTPException(status_code=401, detail="Erro na validação do token")