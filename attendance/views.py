from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Attendance
from students.models import StudentProfile
from courses.models import Course


@login_required(login_url='login')
def attendance_report(request):
    """Attendance report for teachers"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    records = Attendance.objects.all().select_related('student')
    
    # Filter by date if provided
    date = request.GET.get('date')
    if date:
        records = records.filter(date=date)
    
    # Filter by course if provided
    course_id = request.GET.get('course')
    if course_id:
        records = records.filter(student__course_id=course_id)
    
    courses = Course.objects.all()
    context = {
        'attendance': records,
        'courses': courses,
        'selected_date': date,
        'selected_course': course_id,
    }
    return render(request, 'attendance/report.html', context)


@login_required(login_url='login')
def student_attendance_view(request):
    """Student view their own attendance"""
    if not request.user.is_student():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    try:
        student = StudentProfile.objects.get(user=request.user)
        records = Attendance.objects.filter(student=student).order_by('-date')
        
        total = records.count()
        present = records.filter(is_present=True).count()
        percentage = (present / total * 100) if total > 0 else 0
        
        context = {
            'attendance': records,
            'total': total,
            'present': present,
            'percentage': percentage,
        }
        return render(request, 'attendance/student_view.html', context)
    except StudentProfile.DoesNotExist:
        return HttpResponseForbidden("Student profile not found.")
