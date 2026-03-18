from django import forms
from .models import Course, Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'code', 'description', 'duration_months')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'code', 'course', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
