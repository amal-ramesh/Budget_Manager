from jose import JWTError,jwt
from datetime import datetime,timedelta
from app.config import settings

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode , settings.secret_key , algorithm=settings.algorithm)
    return encoded_jwt

