from django.db import models


class Course(models.Model):
    """Course Model"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(default='', blank=True)
    duration_months = models.IntegerField(default=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    """Subject Model"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['course', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.course.code})"
