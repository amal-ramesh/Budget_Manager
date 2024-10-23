
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.auth.authorise import create_access_token, blacklist_token, verify_password, get_password_hash, verify_token
from app.schema import Token, RegisterSchema, LoginSchema
from app.models import User, UserInDB
from app.database import user_collection,login_token_collection
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.auth.authorise import blacklist
from app.schema import Tags

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

login_data_temp_storage = []

# Register new user
@router.post("/register", response_model=Token,tags=[Tags.users])
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
@router.post("/login", response_model=Token,tags=[Tags.users])
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
    # login_token_collection.insert_one({"token": access_token, "username": user["username"]})
    login_data_temp_storage.append(access_token)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout",tags=[Tags.users])
async def logout(token: str):
    # login_token_list = [doc["token"] for doc in login_token_collection.find({}, {"token": True})]
    # print(login_token_list)
    if token not in login_data_temp_storage:
        return {"Message":"Such a token do not exist"}
    elif token in blacklist:
        return {"message":"Already used token"}
    blacklist_token(token)  # Blacklist the current token
    login_token_collection.delete_many({"token":token})
    return {"message": "Successfully logged out"}

