from django.db import models
from students.models import StudentProfile


class Attendance(models.Model):
    """Attendance Model"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    remarks = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('student', 'date')
        ordering = ['-date']
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.user.get_full_name()} - {self.date} ({status})"
