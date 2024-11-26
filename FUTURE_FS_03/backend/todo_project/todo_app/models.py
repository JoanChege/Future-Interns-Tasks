from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link tasks to a user
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
