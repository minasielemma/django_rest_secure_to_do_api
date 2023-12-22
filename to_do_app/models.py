from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plan(models.Model):
    plan_name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)
    fetch_count = models.IntegerField(default=0)
    channel_name = models.CharField(max_length=100, unique=True, null=True)
    class Meta:
        unique_together =("plan_name", "owner")
        indexes = [
            models.Index(fields=['plan_name', 'owner']),
            models.Index(fields=['created_at', 'modified_at']),
        ]

class Task(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fetch_count = models.IntegerField(default=0)
    channel_name = models.CharField(max_length=100, unique=True, null=True)
    class Meta:
        unique_together = ("plan", "task_name")
        indexes = [
            models.Index(fields=['plan', 'task_name']),
            models.Index(fields=['created_at', 'modified_at']),
        ]