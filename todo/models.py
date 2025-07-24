from django.db import models 
from django.utils import timezone 

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
