# from fastapi import HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError,jwt
# from datetime import datetime,timedelta
#
# from starlette import status
#
# from app.config import settings
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
#
# def create_access_token(data:dict):
#     to_encode = data.copy()
#     expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
#     to_encode.update({"exp":expire})
#     encoded_jwt = jwt.encode(to_encode , settings.secret_key , algorithm=settings.algorithm)
#     return encoded_jwt
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         # Decode the JWT token
#         payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
#
#     # Fetch the user from the database using the email
#     user = await get_user_by_email(email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user







from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError
from app.database import user_collection

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# In-memory token blacklist for logout functionality
blacklist = set()

# Helper to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
def verify_token(token: str):
    if token in blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Blacklist a token (for logout)
def blacklist_token(token: str):
    blacklist.add(token)

# Hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


