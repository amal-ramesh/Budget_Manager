from pymongo import MongoClient

client = MongoClient("mongodb+srv://amalrameshofficial01:Budgetmanagement@budgetcluster.038bv.mongodb.net/?retryWrites=true&w=majority&appName=BudgetCluster")

db = client.budget_mangement