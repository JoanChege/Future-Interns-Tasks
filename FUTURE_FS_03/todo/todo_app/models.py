from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    due_date = models.DateField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.title