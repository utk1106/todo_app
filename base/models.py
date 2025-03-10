from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True) #added for cron job
    reminded = models.BooleanField(default=False)  # Added for cron job

    #after adding due_date and reminded and running python3 manage.py makemigrations, migration folder added new field
    # and after than running python3 manage.py migrate, the new field was added to the database sql3

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete', 'due_date']
