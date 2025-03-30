from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    
