from typing import List


def individual_serializer_user(user) -> dict:
    return {
        "id" : str(user["_id"]),
        "User Name" : str(user["username"]),
        "Email" : str(user["email"])
    }

def list_serial_user(users) -> list:
    return [individual_serializer_user(user) for user in users]


def individual_serializer_budget(budget) -> dict:
    return {
        "id" : str(budget["_id"]),
        "Budget ID" : str(budget["budget_id"]),
        "User ID" : str(budget["user_id"]),
        "Name" : str(budget["name"]),
        "Month" : str(budget["month"]),
        "Total Income" : str(budget["total_income"]),
        "Total Expense" : str(budget["total_expense"]),
        "Expenses" : budget["expenses"]
    }

def list_serial_budget(budgets) -> list:
    return [individual_serializer_budget(budget) for budget in budgets]


def individual_serializer_expense(expense) -> dict:
    return {
        "id" : str(expense["_id"]),
        "Budget ID" : str(expense["budget_id"]),
        "Amount" : str(expense["amount"]),
        "Category" : str(expense["category"])
    }

def list_serial_expense(expenses) -> list:
    return [individual_serializer_expense(expense) for expense in expenses]

def individual_serializer_income(income) -> dict:
    return {
        "id" : str(income["_id"]),
        "Budget ID" : str(income["budget_id"]),
        "Amount" : str(income["amount"]),
        "Description" : str(income["description"])
    }

def list_serial_income(incomes) -> list:
    return [individual_serializer_income(income) for income in incomes]