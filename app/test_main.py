# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from app.auth.authorise import create_access_token, verify_token
# from app.database import user_collection
#
# client = TestClient(app)
#
# # Demo data created
# test_user = {
#     "username": "testuser",
#     "email": "testuser@gmail.com",
#     "password": "testpassword",
#     "two_factor_enabled": False
# }
#
# @pytest.fixture(autouse=True)
# def setup_and_teardown():
#     # To remove test data before running
#     user_collection.delete_many({"email": test_user["email"]})
#
#     # To remove test data after running
#     yield
#     user_collection.delete_many({"email": test_user["email"]})
#
#
# # Test User Registration
# def test_register_user():
#     response = client.post("/auth/register", json=test_user)
#     assert response.status_code == 201  # User created successfully
#     assert response.json()["message"] == "User created successfully"
#
#
# # Test User Login
# def test_login_user():
#     # First, register the user
#     client.post("/auth/register", json=test_user)
#
#     # Now login with the registered user
#     login_data = {
#         "username": test_user["username"],
#         "password": test_user["password"]
#     }
#     response = client.post("/auth/login", data=login_data)
#     assert response.status_code == 200  # Successful login
#     json_response = response.json()
#     assert "access_token" in json_response  # Token is returned
#
#     # Verify token
#     token = json_response["access_token"]
#     decoded_token = verify_token(token)
#     assert decoded_token is not None  # Token should be valid
#
#
# # Test User Logout
# def test_logout_user():
#     # First, register the user
#     client.post("/auth/register", json=test_user)
#
#     # Login to get the token
#     login_data = {
#         "username": test_user["username"],
#         "password": test_user["password"]
#     }
#     login_response = client.post("/auth/login", data=login_data)
#     token = login_response.json()["access_token"]
#
#     # Logout with the token
#     headers = {"Authorization": f"Bearer {token}"}
#     logout_response = client.post("/auth/logout", headers=headers)
#
#     assert logout_response.status_code == 200
#     assert logout_response.json() == {"message": "Successfully logged out"}
#
#     # Try logging out again with the same token (should be blacklisted)
#     second_logout_response = client.post("/auth/logout", headers=headers)
#     assert second_logout_response.status_code == 401
#     assert second_logout_response.json()["detail"] == "Invalid token"
#
#
# # Test Invalid Login Attempt
# def test_invalid_login():
#     # Try logging in with wrong credentials
#     login_data = {
#         "username": "wronguser",
#         "password": "wrongpassword"
#     }
#     response = client.post("/auth/login", data=login_data)
#     assert response.status_code == 401
#     assert response.json()["detail"] == "Incorrect username or password"



from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import user_collection



client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # To remove test data before running
    user_collection.delete_many({"email": test_user["email"]})

    # To remove test data after running
    yield
    user_collection.delete_many({"email": test_user["email"]})

# Sample user data for tests
test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}

def test_register_user():
    # Test registering a new user
    response = client.post("/register", json=test_user)
    assert response.status_code == 200  # Success when registering
    json_response = response.json()
    assert "access_token" in json_response  # JWT token should be in response
    assert json_response["token_type"] == "bearer"  # Token type should be bearer


def test_login_user():
    # First, register the user
    client.post("/register", json=test_user)

    # Now login with the registered user
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 200  # Successful login
    json_response = response.json()
    assert "access_token" in json_response  # JWT token should be in response
    assert json_response["token_type"] == "bearer"  # Token type should be bearer

    # Save the token for use in the logout test
    global access_token
    access_token = json_response["access_token"]


# def test_logout_user():
#     # First, register and log in the user to get the token
#     client.post("/register", json=test_user)
#     login_data = {
#         "username": test_user["username"],
#         "password": test_user["password"]
#     }
#     login_response = client.post("/login", data=login_data)
#     access_token = login_response.json()["access_token"]
#
#     # Now test the logout with the token
#     # response = client.post("/logout", json={"token": access_token})
#     response = client.post("/logout", data = access_token)
#
#     assert response.status_code == 200  # Successful logout
#     # json_response = response.json()
#     assert response.json() == {"message" : "Successfully logged out"}


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
    response = client.post(f"/logout?token={access_token}")

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

