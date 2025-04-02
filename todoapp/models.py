from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Make sure user is here
    
    def __str__(self):
        return self.title