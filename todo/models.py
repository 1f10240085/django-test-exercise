from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    posted_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt