from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date', 'is_present', 'remarks')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
