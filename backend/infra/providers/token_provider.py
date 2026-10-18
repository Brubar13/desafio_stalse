from datetime import datetime, timedelta
from time import time
import os
from dotenv import load_dotenv

load_dotenv()

from jose import jwt

#CONFIG
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_IN_MINUTES = int(os.getenv("EXPIRE_IN_MINUTES"))
EXPIRE_REFRESH_IN_MINUTES = int(os.getenv("EXPIRE_REFRESH_IN_MINUTES"))

def createAcessToken(data: dict):
    dados = data.copy()

    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRE_IN_MINUTES)
    expiracaoRefresh = datetime.utcnow() + timedelta(minutes=EXPIRE_REFRESH_IN_MINUTES)

    dados.update({'exp': expiracao})

    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

    dadosRefresh = data.copy()

    dadosRefresh.update({'exp': expiracaoRefresh})

    refresh_token = jwt.encode(dadosRefresh, SECRET_KEY, algorithm=ALGORITHM)

    return {'token': token_jwt, 'refreshToken': refresh_token}

def validateAcessToken(token: str):
    validate = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return validate.get('sub')