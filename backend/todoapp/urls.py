from django.urls import path
from .views import list_todos, add_todo

urlpatterns = [
    path('todos/add/', add_todo),
    path('todos/', list_todos),
]