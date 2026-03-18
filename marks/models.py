from django.db import models
from students.models import StudentProfile
from courses.models import Subject


class Result(models.Model):
    """Result/Marks Model"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    grade = models.CharField(max_length=2, default='F')  # A, B, C, D, F
    remarks = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        unique_together = ('student', 'subject')
        ordering = ['-subject']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name}: {self.marks}"
    
    def save(self, *args, **kwargs):
        """Auto calculate grade based on marks"""
        if self.marks >= 90:
            self.grade = 'A'
        elif self.marks >= 80:
            self.grade = 'B'
        elif self.marks >= 70:
            self.grade = 'C'
        elif self.marks >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)
