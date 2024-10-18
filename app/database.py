from pymongo import MongoClient

client = MongoClient("mongodb+srv://amalrameshofficial01:budgetmanager@budgetcluster.038bv.mongodb.net/?retryWrites=true&w=majority&appName=BudgetCluster")

db = client.budget_mangement

budget_collection = db.budget
income_collection = db.income
expense_collection = db.expense
user_collection = db.user