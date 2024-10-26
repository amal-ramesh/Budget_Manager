from enum import Enum

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class LoginSchema(BaseModel):
    username: str
    password: str

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class Tags(Enum):
    budgets = "Budgets"
    users = "Users"
    income = "Income"
    expense = "Expense"
    category = "Category"
    report = "Report"
    starred = "Important(Starred)"
    profile = "Profile"
