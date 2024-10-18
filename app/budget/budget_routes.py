from app.models import User,Budget,Expense,Income
from fastapi import APIRouter
from app.database import budget_collection,income_collection,expense_collection
from app.serialization import *



budget_router = APIRouter()

@budget_router.post("/create_budget")
async def create_budget_new(budget_data : Budget):
    budget_collection.insert_one(dict(budget_data))
    return {"Message":"Budget added successfully !"}


@budget_router.post("/add_income")
async def add_income(income_data:Income):
    income_collection.insert_one(income_data.dict())
    budget_id = income_data.budget_id
    budget_id_list = [doc["budget_id"] for doc in budget_collection.find({}, {"budget_id": True})]
    if budget_id in budget_id_list:
        budget_collection.find_one_and_update({"budget_id":budget_id},{"$inc":{"total_income":income_data.amount}})
    return {"Message":"Income added successfully"}

@budget_router.post("/add_expense")
async def add_expense(expense_data:Expense):
    expense_collection.insert_one(expense_data.dict())
    budget_id = expense_data.budget_id
    budget_id_list = [doc["budget_id"] for doc in budget_collection.find({}, {"budget_id": True})]
    if budget_id in budget_id_list:
        budget_collection.find_one_and_update({"budget_id":budget_id},{"$inc":{"total_expense":expense_data.amount}})

    curr_category_list = budget_collection.find({"budget_id":budget_id},{"expenses":True})
    if expense_data.category not in curr_category_list:
        budget_collection.find_one_and_update({"budget_id":budget_id},{"$push":{"expenses":expense_data.category}})

    return {"Message":"Expense added successfully"}



# @budget_router.get("/show_budget/{month}")
# async def show_budget_with_month(month:str):
#     budget_req = list_serial_budget(budget_collection.find_one({"month":month}))
#     return budget_req

@budget_router.get("/budget")
async def view_budget():
    budget_list = list_serial_budget(budget_collection.find())
    return budget_list



#Category wise expense

@budget_router.get("/category")
async def category_details(given_category:str):
    expense_list = [doc["amount"] for doc in expense_collection.find({"category":given_category}, {"amount": True})]
    total_expense = sum(expense_list)
    return {f"Total expense of {given_category} : {total_expense}"}

#Monthly report which contains Total income of the month and total expense of the month

@budget_router.get("/monthly_report")
async def monthly_report(given_month:str):
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

@budget_router.get("/budget_summary")
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