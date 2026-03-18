from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    (1, 'Teacher'),
    (2, 'Student'),
)


class User(AbstractUser):
    """Custom User Model with role support"""
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_teacher(self):
        return self.role == 1
    
    def is_student(self):
        return self.role == 2
