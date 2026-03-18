from django.db import models
from django.conf import settings


class Notice(models.Model):
    """Notice board posts published by teachers."""

    title = models.CharField(max_length=160)
    message = models.TextField()
    audience = models.CharField(
        max_length=20,
        choices=(('all', 'All'), ('students', 'Students'), ('teachers', 'Teachers')),
        default='all',
    )
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    publish_until = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='published_notices',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
