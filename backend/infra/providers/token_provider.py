from datetime import datetime, timedelta
from time import time

from jose import jwt

#CONFIG´s
SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY5MTQyMDA1OSwiaWF0IjoxNjkxNDIwMDU5fQ.GfHGTlkXIQg_2yoQwgfhpMH7hHepNeRemAbduzioWoo"
ALGORITHM = "HS256"
EXPIRE_IN_MINUTES = 24 * 7 * 60
EXPIRE_REFRESH_IN_MINUTES = 24 * 8 * 60


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