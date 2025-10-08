from django.db import models

class Todo(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    marked_as_done_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']  # Show newest first

    def __str__(self):
        return f"{self.content[:50]}..."

    @property
    def is_done(self):
        return self.marked_as_done_at is not None
