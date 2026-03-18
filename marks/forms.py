from django import forms
from .models import Result


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('student', 'subject', 'marks', 'remarks')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
