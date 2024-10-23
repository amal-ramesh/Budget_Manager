# from fastapi import APIRouter,Depends,HTTPException,status
# from app.auth.authorise import create_access_token
# from app.auth.hashing import Hash
# from app.database import user_collection
# from app.models import User
#
#
# auth_router = APIRouter()
# @auth_router.post("/register")
# async def register(user_data:User):
#     hashed_password = Hash.bcrypt(user_data.password)
#     user_data.password = hashed_password
#     user_collection.insert_one(user_data.dict())
#     return {"Message":"User Registered Successfully !"}
#
# @auth_router.post("/login")
# async def login(username:str , password:str):
#     user = user_collection.find_one({"username":username})
#     if not user or not Hash.verify(user["password"],password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
#     access_token = create_access_token(data={"sub":user["username"]})
#     return {"Access Token":access_token,"Token Type":"bearer"}


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.auth.authorise import create_access_token, blacklist_token, verify_password, get_password_hash, verify_token
from app.schema import Token, RegisterSchema, LoginSchema
from app.models import User, UserInDB
from app.database import user_collection
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Register new user
@router.post("/register", response_model=Token)
async def register(user: RegisterSchema):
    # Check if the user already exists in the database
    existing_user = user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Store the new user in MongoDB
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,  # Store the hashed password
        "two_factor_enabled": False
    }
    user_collection.insert_one(user_data)

    # Create a JWT token for the new user
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


# Login route
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a JWT token for the user
    access_token = create_access_token(data={"sub": user["username"]})

    return {"access_token": access_token, "token_type": "bearer"}


# Logout route
@router.post("/logout")
async def logout(token: str = Depends(verify_token)):
    blacklist_token(token)  # Blacklist the current token
    return {"message": "Successfully logged out"}
