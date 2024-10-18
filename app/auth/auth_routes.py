from fastapi import APIRouter,Depends,HTTPException,status
from app.auth.oauth2 import create_access_token
from app.auth.hashing import Hash
from app.database import user_collection
from app.models import User


auth_router = APIRouter()
@auth_router.post("/register")
async def register(user_data:User):
    hashed_password = Hash.bcrypt(user_data.password)
    user_data.password = hashed_password
    user_collection.insert_one(user_data.dict())
    return {"Message":"User Registered Successfully !"}

@auth_router.post("/login")
async def login(username:str , password:str):
    user = user_collection.find_one({"username":username})
    if not user or not Hash.verify(user["password"],password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    access_token = create_access_token(data={"sub":user["username"]})
    return {"Access Token":access_token,"Token Type":"bearer"}
