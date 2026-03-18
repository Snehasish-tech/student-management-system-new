from django import forms
from .models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'message', 'audience', 'is_pinned', 'is_active', 'publish_until']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notice title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write notice details'}),
            'audience': forms.Select(attrs={'class': 'form-select'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'publish_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
