from django.db import models
from accounts.models import User


class StudentProfile(models.Model):
    """Extended Student Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    roll_number = models.CharField(max_length=20, unique=True)
    college_id = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True)
    about = models.TextField(default='', blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"
