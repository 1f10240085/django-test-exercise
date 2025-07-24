from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

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
    tags = models.ManyToManyField(Tag, blank=True)  # タグ機能追加！

    class Meta:
        ordering = ['order']

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
