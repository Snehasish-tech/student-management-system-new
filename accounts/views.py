from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import UserSignUpForm, UserLoginForm, UserProfileForm
from .models import User
from courses.models import Course
from notices.models import Notice
from students.models import StudentProfile
from teachers.models import TeacherProfile


@require_http_methods(["GET", "POST"])
def signup(request):
    """User Registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Ensure role profile exists so first login never fails on dashboards.
            if user.is_teacher():
                TeacherProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'employee_id': f"T{user.id:04d}",
                        'subject': 'General Studies',
                        'qualification': 'N/A',
                        'experience': 0,
                    },
                )
            else:
                StudentProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'roll_number': f"R{user.id:04d}",
                        'college_id': f"CID{user.id:05d}",
                    },
                )

            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! You are signed up successfully.')
            
            if user.is_teacher():
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserSignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User Login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                if user.is_teacher():
                    return redirect('teacher_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    """User Logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def profile(request):
    """User Profile View"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


def home(request):
    """Landing Page"""
    latest_notices = Notice.objects.filter(is_active=True).order_by('-is_pinned', '-created_at')[:4]
    context = {
        'total_students': User.objects.filter(role=2).count(),
        'total_teachers': User.objects.filter(role=1).count(),
        'total_courses': Course.objects.count(),
        'latest_notices': latest_notices,
    }
    return render(request, 'accounts/home.html', context)
