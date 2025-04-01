import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_add_todo():
    # Create a user for authentication
    user = User.objects.create_user(username="testuser", password="password123")

    # Log in to get the token
    client = APIClient()
    login_data = {"username": "testuser", "password": "password123"}
    response = client.post("/api/auth/login/", login_data, format="json")

    # Print the response for debugging
    print(f"Login Response: {response.status_code}, {response.data}")

    # Get the access token from the response
    access_token = response.data.get('access')  # Get the access token

    # Ensure the access token exists
    assert access_token is not None, "Login failed: No access token received"

    # Use the access token to authenticate the request
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    todo_data = {"title": "New Todo", "description": "Testing add API", "completed": False}
    response = client.post("/api/todos/add/", todo_data, format="json")

    assert response.status_code == 201  # Status code should be 201 (created)
    assert response.data["title"] == "New Todo"
    assert response.data["description"] == "Testing add API"
