from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import StudentProfile
from marks.models import Result
from attendance.models import Attendance
from .forms import StudentProfileForm


def _get_or_create_student_profile(user):
    return StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'roll_number': f"R{user.id:04d}",
            'college_id': f"CID{user.id:05d}",
        },
    )[0]


@login_required(login_url='login')
def student_dashboard(request):
    """Student Dashboard - View Only"""
    if not request.user.is_student():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = _get_or_create_student_profile(request.user)
    results = Result.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)
    
    context = {
        'student': student,
        'results': results,
        'attendance': attendance,
    }
    return render(request, 'students/dashboard.html', context)


@login_required(login_url='login')
def student_profile(request):
    """Student Profile View"""
    if not request.user.is_student():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = _get_or_create_student_profile(request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/profile.html', {'student': student, 'form': form, 'message': 'Profile updated!'})
    else:
        form = StudentProfileForm(instance=student)
    
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'students/profile.html', context)


@login_required(login_url='login')
def student_attendance(request):
    """View Student Attendance"""
    if not request.user.is_student():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = _get_or_create_student_profile(request.user)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    
    # Calculate attendance percentage
    total_days = attendance.count()
    present_days = attendance.filter(is_present=True).count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    context = {
        'student': student,
        'attendance': attendance,
        'attendance_percentage': attendance_percentage,
        'total_days': total_days,
        'present_days': present_days,
    }
    return render(request, 'students/attendance.html', context)


@login_required(login_url='login')
def student_results(request):
    """View Student Results"""
    if not request.user.is_student():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = _get_or_create_student_profile(request.user)
    results = Result.objects.filter(student=student)
    
    # Calculate average marks
    if results.exists():
        avg_marks = sum([r.marks for r in results]) / len(results)
        avg_marks = round(avg_marks, 2)
    else:
        avg_marks = 0
    
    context = {
        'student': student,
        'results': results,
        'avg_marks': avg_marks,
    }
    return render(request, 'students/results.html', context)
