import pytest
from todoapp.models import Todo

@pytest.mark.django_db
def test_todo_creation():
    todo = Todo.objects.create(title="Test Todo", description="This is a test", completed=False)
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test"
    assert not todo.completed
