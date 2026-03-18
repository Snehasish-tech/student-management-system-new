from django.db import models
from accounts.models import User


class TeacherProfile(models.Model):
    """Teacher Profile Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)
    bio = models.TextField(default='', blank=True)
    profile_picture = models.ImageField(upload_to='teachers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.subject})"
