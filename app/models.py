#Creating models for User , Expense and Budget

from pydantic import BaseModel, Field, EmailStr, validator
from bson import ObjectId
from typing import List, Optional, Literal



class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    two_factor_enabled: bool = False

class UserInDB(User):
    hashed_password: str

class Budget(BaseModel):
    budget_id : str
    user_id : str
    name : str
    month : str
    total_income : float
    total_expense : float = 0
    expenses : List[str] = []
    important : bool = False
    owner: Optional[str] = None

    @validator('month')
    def convert_month_to_lowercase(cls, v):
        return v.lower()


class Expense(BaseModel):
    id : str
    budget_id : str
    amount : float
    category : str


class CategoryLimit(BaseModel):
    category : str
    limit : float


class Income(BaseModel):
    id : str
    budget_id : str
    amount : float
    description : str


class CategorySum(BaseModel):
    category:str
    sum:float=0

