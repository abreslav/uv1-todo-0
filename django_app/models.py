from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    marked_as_done_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']  # Show newest first

    def __str__(self):
        return f"{self.content[:50]}..."

    @property
    def is_done(self):
        return self.marked_as_done_at is not None

    @property
    def is_deleted(self):
        return self.deleted_at is not None
