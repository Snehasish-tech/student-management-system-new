from django import forms
from .models import TeacherProfile
from students.models import StudentProfile
from courses.models import Course


class TeacherProfileForm(forms.ModelForm):
    """Teacher Profile Form"""
    
    class Meta:
        model = TeacherProfile
        fields = ('employee_id', 'subject', 'qualification', 'experience', 'bio', 'profile_picture')
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StudentManagementForm(forms.ModelForm):
    """Form to manage students"""
    
    class Meta:
        model = StudentProfile
        fields = ('roll_number', 'college_id', 'course', 'about')
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'college_id': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
