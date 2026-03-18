from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, ROLE_CHOICES


class UserSignUpForm(UserCreationForm):
    """Sign up form with role selection"""
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Select Your Role"
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "At least 8 characters"
        self.fields['password2'].help_text = "Confirm password"


class UserLoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(UserChangeForm):
    """Profile update form"""
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
