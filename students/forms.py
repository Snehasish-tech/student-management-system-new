from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    """Student Profile Update Form (VIEW ONLY - except profile picture)"""
    
    class Meta:
        model = StudentProfile
        fields = ('roll_number', 'college_id', 'about', 'profile_picture')
        widgets = {
            'roll_number': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'college_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
