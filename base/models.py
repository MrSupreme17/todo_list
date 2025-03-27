from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # ForeignKey creates a link between a task and a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    # The title of the task (a short string)
    title = models.CharField(max_length=200)  
    # A description for the task (optional text field)
    description = models.TextField(null=True, blank=True)  
    # Boolean field to mark task as complete or not (defaults to False)
    complete = models.BooleanField(default=False)  
    # Automatically set the task creation date and time when a task is created
    create = models.DateTimeField(auto_now_add=True)  

    # Add a field to store the due date for a task (optional)
    due_date = models.DateField(null=True, blank=True)  

    # This method returns the title of the task when it's called (e.g., in the admin panel)
    def __str__(self):
        return self.title  

    class Meta:
        # The ordering will show tasks based on their completion status
        ordering = ['complete']  # Inomplete tasks will be shown first
