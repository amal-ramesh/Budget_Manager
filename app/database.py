from pymongo import MongoClient

client = MongoClient("mongodb+srv://amalrameshofficial01:budgetmanager@budgetcluster.038bv.mongodb.net/?retryWrites=true&w=majority&appName=BudgetCluster")

db = client.budget_mangement

budget_collection = db.budget
income_collection = db.income
expense_collection = db.expense
user_collection = db.user
category_limit_collection = db.category_limit
category_sum_collection = db.category_sum
login_token_collection = db.login_token