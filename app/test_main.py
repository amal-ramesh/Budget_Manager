
from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import user_collection,budget_collection,income_collection,expense_collection

access_token = None
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # To remove test data before running
    user_collection.delete_many({"email": test_user["email"]})
    budget_collection.delete_many({"budget_id":test_budget["budget_id"]})
    income_collection.delete_many({"id":test_income["id"]})
    expense_collection.delete_many({"id":test_expense["id"]})


    # To remove test data after running
    yield
    user_collection.delete_many({"email": test_user["email"]})
    budget_collection.delete_many({"budget_id": test_budget["budget_id"]})
    income_collection.delete_many({"id": test_income["id"]})
    expense_collection.delete_many({"id": test_expense["id"]})

@pytest.fixture
def auth_token():
    # Register user and get token for authentication
    client.post("/register", json=test_user)
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/login", data=login_data)
    access_token = login_response.json().get("access_token")
    assert access_token is not None, "Login failed, no access token returned."
    return access_token


# Sample user data for tests
test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}

def test_register_user():
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_login_user():
    client.post("/register", json=test_user)

    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"
    # global access_token
    access_token = response.json()["access_token"]
    return access_token



def test_logout_user():
    # First, register and log in the user to get the token
    client.post("/register", json=test_user)
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/login", data=login_data)
    access_token = login_response.json()["access_token"]

    # Now test the logout by passing the token as a query parameter
    response = client.post(f"/logout",headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200  # Successful logout
    assert response.json() == {"message": "Successfully logged out"}


def test_invalid_login():
    # Try logging in with incorrect credentials
    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 401  # Unauthorized
    json_response = response.json()
    assert json_response["detail"] == "Incorrect username or password"


test_budget = {
    "budget_id" : "testbudgetid",
    "user_id" : "testuserid",
    "name" : "testbugetname",
    "month" : "january",
    "total_income" : 1000,
    "total_expense" : 200,
    "expenses" : ["food"],
    "important" : False,
    "owner":""
}


test_income = {
    "id" : "testincomeid",
    "budget_id" : "testbudgetid",
    "amount" : 500,
    "description" : "testdescriptionofincome"
}

test_expense = {
    "id" : "testexpenseid",
    "budget_id" : "testbudgetid",
    "amount" : 100,
    "category" : "food"
}
def test_create_budget(auth_token):

    test_budget["owner"] = test_user["username"]

    response = client.post("/create_budget",json=test_budget,headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json() == {"Message":"Budget added successfully !"}

def test_add_income(auth_token):
    client.post("/create_budget", json=test_budget,headers={"Authorization": f"Bearer {auth_token}"})
    response = client.post("/add_income",json=test_income,headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json() == {"Message":"Income added successfully"}

def test_add_expense(auth_token):
    client.post("/create_budget", json=test_budget,headers={"Authorization": f"Bearer {auth_token}"})
    client.post("/add_income",json=test_income,headers={"Authorization": f"Bearer {auth_token}"})

    response = client.post("/add_expense",json=test_expense,headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json() == {"Message":"Expense added successfully"}

