from django.db import models
from django.contrib.auth.models import User
import markdown
from django.utils.safestring import mark_safe

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
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

    @property
    def content_html(self):
        """Render content as HTML from Markdown"""
        md = markdown.Markdown(extensions=['nl2br', 'fenced_code'])
        return mark_safe(md.convert(self.content))
