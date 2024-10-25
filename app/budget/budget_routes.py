from enum import Enum
from typing import Literal

from bson import ObjectId

from app.models import User,Budget,Expense,Income,CategoryLimit,CategorySum
from fastapi import APIRouter, HTTPException, Depends
from app.database import budget_collection,income_collection,expense_collection,category_limit_collection,category_sum_collection,user_collection
from app.serialization import *
from app.schema import Tags


budget_router = APIRouter()



@budget_router.post("/create_budget",tags=[Tags.budgets])
async def create_budget_new(budget_data : Budget):
    budget_collection.insert_one(dict(budget_data))
    return {"Message":"Budget added successfully !"}


@budget_router.post("/add_income",tags=[Tags.income])
async def add_income(income_data:Income):
    income_collection.insert_one(income_data.dict())
    budget_id = income_data.budget_id
    budget_id_list = [doc["budget_id"] for doc in budget_collection.find({}, {"budget_id": True})]
    if budget_id in budget_id_list:
        budget_collection.find_one_and_update({"budget_id":budget_id},{"$inc":{"total_income":income_data.amount}})
    return {"Message":"Income added successfully"}

@budget_router.post("/add_expense",tags=[Tags.expense])
async def add_expense(expense_data:Expense):

    categories = [doc["category"] for doc in category_limit_collection.find({}, {"category": True})]

    if expense_data.category in categories:
        category_limit_list = [doc["limit"] for doc in category_limit_collection.find({"category":expense_data.category}, {"limit": True})]
        category_limit = sum(category_limit_list)

    else:
        category_limit = float("inf")

    category_sum_list = [doc["sum"] for doc in category_sum_collection.find({"category":expense_data.category}, {"sum": True})]
    category_sum = sum(category_sum_list)

    if expense_data.amount + category_sum > category_limit:
        raise HTTPException(status_code=400, detail="Category limit exceeded")
    
    expense_collection.insert_one(expense_data.dict())
    budget_id = expense_data.budget_id
    budget_id_list = [doc["budget_id"] for doc in budget_collection.find({}, {"budget_id": True})]
    if budget_id in budget_id_list:
        budget_collection.find_one_and_update({"budget_id":budget_id},{"$inc":{"total_expense":expense_data.amount}})

    curr_category_list = budget_collection.find({"budget_id":budget_id},{"expenses":True})
    if expense_data.category not in curr_category_list:
        budget_collection.find_one_and_update({"budget_id":budget_id},{"$push":{"expenses":expense_data.category}})

    category_sum_collection.update_one(
        {"category": expense_data.category},
        {"$inc": {"sum": expense_data.amount}},
        upsert=True
    )


    return {"Message":"Expense added successfully"}


@budget_router.get("/all_budget",tags=[Tags.budgets])
async def view_all_budget():
    budget_list = list_serial_budget(budget_collection.find())
    return budget_list


@budget_router.get("/budget_by_id",tags=[Tags.budgets])
async def view_budget_by_id(budget_id:str):
    # budget_list = list_serial_budget(budget_collection.find())
    # return budget_list
    budget_req = budget_collection.find_one({"budget_id":budget_id})

    if not budget_req:
        raise HTTPException(status_code=404 , detail="Budget ID Invalid")

    if "_id" in budget_req:
        budget_req["_id"] = str(budget_req["_id"])

    return budget_req



#Category wise expense

@budget_router.get("/category",tags=[Tags.category])
async def category_details(given_category:str):
    expense_list = [doc["amount"] for doc in expense_collection.find({"category":given_category}, {"amount": True})]
    total_expense = sum(expense_list)
    return {f"Total expense of {given_category} : {total_expense}"}

#Monthly report which contains Total income of the month and total expense of the month

@budget_router.get("/monthly_report",tags=[Tags.report])
async def monthly_report(given_month:Literal["january","february","march","april","may","june","july","august","september","october","november","december"]):
    income_list = [doc["total_income"] for doc in budget_collection.find({"month":given_month}, {"total_income": True})]
    total_income_monthly = sum(income_list)

    expense_list = [doc["total_expense"] for doc in budget_collection.find({"month": given_month}, {"total_expense": True})]
    total_expense_monthly = sum(expense_list)

    # return {f"""#### Summary of {given_month} ####
    #         #Total income : {total_income_monthly}
    #         #Total expense : {total_expense_monthly}"""}

    return {
        "Summary of" : given_month ,
        "Total Income" : total_income_monthly,
        "Total Expense" : total_expense_monthly
    }

#To show total income , total expense and Balance amount of a budget

@budget_router.get("/budget_summary",tags=[Tags.budgets])
async def budget_summary(given_budget_id:str):
    # tot_income =  budget_collection.find_one({"budget_id":given_budget_id},{"total_income":True})
    # tot_expense = budget_collection.find_one({"budget_id":given_budget_id},{"total_expense":True})
    # balance = tot_income - tot_expense

    tot_income_list = [doc["total_income"] for doc in budget_collection.find({"budget_id":given_budget_id}, {"total_income": True})]
    tot_income = sum(tot_income_list)



    tot_expense_list = [doc["total_expense"] for doc in budget_collection.find({"budget_id": given_budget_id}, {"total_expense": True})]
    tot_expense = sum(tot_expense_list)

    balance = tot_income-tot_expense

    return {
        "Total Income":tot_income,
        "Total Expense":tot_expense,
        "Balance Amount":balance
    }

@budget_router.post("/category_limit",tags=[Tags.category])
async def add_category_limit(category_data:CategoryLimit):
    category_limit_collection.update_one(
        {"category": category_data.category},
        {"$set": {"limit": category_data.limit}},
        upsert=True
    )
    return {"message": f"Limit set for {category_data.category}"}

@budget_router.get("/important_notification",tags=[Tags.starred])
async def get_important_budgets():
    important_budgets = list_serial_budget(budget_collection.find({"important":True}))
    return important_budgets

@budget_router.put("/edit_email",tags=[Tags.profile])
async def edit_email_address(user_name:str,new_email:str):
    user_collection.update_one({"username":user_name},{"$set":{"email":new_email}})
    return {"Message":"E-mail edited successfully !"}


#view all income
@budget_router.get("/all_income",tags=[Tags.income])
async def view_all_income(given_budget_id:str):
    all_income = [doc["amount"] for doc in income_collection.find({"budget_id":given_budget_id},{"amount":True})]
    return all_income

#update an already added income

@budget_router.put("/update_income",tags=[Tags.income])
async def update_already_added_income(given_income_id:str , updated_income:float):
    income_id_list = [doc["id"] for doc in income_collection.find({}, {"id": True})]

    if given_income_id in income_id_list:

        old_income_list = [doc["amount"] for doc in income_collection.find({"id":given_income_id},{"amount":True})]
        old_income = sum(old_income_list)


        income_collection.update_one({"id":given_income_id},{"$set":{"amount":updated_income}})

        budget_id_list = [doc["budget_id"] for doc in income_collection.find({"id":given_income_id},{"budget_id":True})]
        budget_id = budget_id_list[0]

        budget_collection.update_one({"budget_id":budget_id},{"$inc":{"total_income":updated_income-old_income}})

        return {"Message":"Income updated successfully !"}

    else:
        return {"Message":"No such income ID exists !"}


#delete an already added income

@budget_router.delete("/delete_income",tags=[Tags.income])
async def delete_income(given_income_id:str):
    income_id_list = [doc["id"] for doc in income_collection.find({}, {"id": True})]

    if given_income_id in income_id_list:

        old_income_list = [doc["amount"] for doc in income_collection.find({"id": given_income_id}, {"amount": True})]
        old_income = sum(old_income_list)

        income_collection.delete_one({"id":given_income_id})

        budget_id_list = [doc["budget_id"] for doc in income_collection.find({"id":given_income_id},{"budget_id":True})]
        budget_id = budget_id_list[0]

        budget_collection.update_one({"budget_id":budget_id},{"$inc":{"total_income":-old_income}})

        return {"Message":"Income deleted successfully !"}

    else:
        return {"Message":"No such income ID exists !"}

