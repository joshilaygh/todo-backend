# Updated tests.py with correct paths

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Todo


# Unit Tests

class TodoModelTest(TestCase):
    
    def test_create_todo(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        todo = Todo.objects.create(
            title="Test Todo",
            description="Test description",
            completed=False,
            user=user 
        )
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test description")
        self.assertFalse(todo.completed)
        self.assertEqual(todo.user, user)

    def test_todo_string_representation(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        
        todo = Todo.objects.create(
            title="Test Todo",
            description="Test description",
            completed=False,
            user=user  # Assign the user here
        )
        # Ensure the string representation of Todo is the title
        self.assertEqual(str(todo), "Test Todo")


# Integration Tests

class UserRegistrationLoginTest(APITestCase):
    
    def test_user_registration_and_login(self):
        # Register a new user
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/auth/register/', registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Registration should be successful
        
        # Log in with the newly registered user
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/auth/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Login should be successful
