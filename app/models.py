#Creating models for User , Expense and Budget

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List,Optional

class User(BaseModel):
    id : str
    username : str
    email : str
    password : str
    two_factor_auth : Optional[bool] = False

    # class Config:
    #     allow_mutation = True

        # class Config:
    #     populate_by_name = True                #allow the model to accept alternative field names, particularly when using aliases for fields.
    #     json_encoders = {ObjectId:str}
    #     json_schema_extra = {
    #         "example": {
    #             "username": "johndoe",
    #             "email": "johndoe@example.com",
    #             "password": "strongpassword",
    #             "two_factor_enabled": False
    #         }
    #     }

class Budget(BaseModel):
    budget_id : str
    user_id : str
    name : str
    month : str
    total_income : float
    total_expense : float = 0
    expenses : List[str] = []

    # class Config:
    #     # populate_by_name = True
    #     # json_encoders = {ObjectId:str}
    #     json_schema_extra = {
    #         "example": {
    #             "budget_id":"10",
    #             "user_id": "60d5f9f5f9f5f9f5f9f5f9f5",
    #             "name": "My Budget",
    #             "month":"January",
    #             "total_income": 5000.0,
    #             "total_expenses": 2000.0,
    #             "expenses": ["Food", "Rent", "Transportation"]
    #         }
    #     }

class Expense(BaseModel):
    id : str
    budget_id : str
    amount : float
    category : str

    # class Config:
    #     populate_by_name = True
    #     json_encoders = {ObjectId:str}
    #     json_schema_extra = {
    #         "example": {
    #             "budget_id": "60d5f9f5f9f5f9f5f9f5f9f5",
    #             "amount": 100.0,
    #             "category": "Food",
    #         }
    #     }

class CategoryLimit(BaseModel):
    category : str
    limit : float


class Income(BaseModel):
    id : str
    budget_id : str
    amount : float
    description : str

    # class Config:
    #     populate_by_name = True
    #     json_encoders = {ObjectId: str}
    #     json_schema_extra = {
    #         "example": {
    #             "budget_id": "60d5f9f5f9f5f9f5f9f5f9f5",
    #             "amount": 100.0,
    #             "description": "Salary"
    #         }
    #     }


class CategorySum(BaseModel):
    category:str
    sum:float=0


# class Notification(BaseModel):
#     notification_type : str = "Important"
