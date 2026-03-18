from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import TeacherProfile
from .forms import TeacherProfileForm, StudentManagementForm
from accounts.models import User
from students.models import StudentProfile
from courses.models import Course
from courses.models import Subject
from attendance.models import Attendance
from marks.models import Result


@login_required(login_url='login')
def teacher_dashboard(request):
    """Teacher Dashboard"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    teacher, _ = TeacherProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'employee_id': f"T{request.user.id:04d}",
            'subject': 'General Studies',
            'qualification': 'N/A',
            'experience': 0,
        },
    )
    students_count = StudentProfile.objects.count()
    courses_count = Course.objects.count()
    
    context = {
        'teacher': teacher,
        'students_count': students_count,
        'courses_count': courses_count,
    }
    return render(request, 'teachers/dashboard.html', context)


@login_required(login_url='login')
def teacher_profile(request):
    """Teacher Profile View/Edit"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    teacher, _ = TeacherProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'employee_id': f"T{request.user.id:04d}",
            'subject': 'General Studies',
            'qualification': 'N/A',
            'experience': 0,
        },
    )
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('teacher_profile')
    else:
        form = TeacherProfileForm(instance=teacher)
    
    context = {
        'teacher': teacher,
        'form': form,
    }
    return render(request, 'teachers/profile.html', context)


# ===== STUDENT MANAGEMENT (CRUD) =====

@login_required(login_url='login')
def manage_students(request):
    """List all students"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    students = StudentProfile.objects.all()
    context = {'students': students}
    return render(request, 'teachers/manage_students.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def add_student(request):
    """Add new student"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        # Create user first
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('add_student')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=2  # Student role
        )
        user.set_password(password)
        user.save()
        
        # Create student profile
        roll_number = request.POST.get('roll_number')
        college_id = request.POST.get('college_id')
        course_id = request.POST.get('course')
        about = request.POST.get('about', '')
        
        student = StudentProfile.objects.create(
            user=user,
            roll_number=roll_number,
            college_id=college_id,
            course_id=course_id if course_id else None,
            about=about
        )
        
        messages.success(request, f'Student {first_name} {last_name} added successfully!')
        return redirect('manage_students')
    
    courses = Course.objects.all()
    form = StudentManagementForm()
    context = {'form': form, 'courses': courses}
    return render(request, 'teachers/add_student.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_student(request, student_id):
    """Edit student"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = get_object_or_404(StudentProfile, user_id=student_id)
    
    if request.method == 'POST':
        # Update student profile fields
        student.roll_number = request.POST.get('roll_number', student.roll_number)
        student.college_id = request.POST.get('college_id', student.college_id)
        course_id = request.POST.get('course')
        if course_id:
            student.course_id = course_id
        student.about = request.POST.get('about', student.about)
        student.save()
        
        # Update user fields
        student.user.first_name = request.POST.get('first_name', student.user.first_name)
        student.user.last_name = request.POST.get('last_name', student.user.last_name)
        student.user.email = request.POST.get('email', student.user.email)
        student.user.save()
        
        messages.success(request, 'Student updated successfully!')
        return redirect('manage_students')
    
    courses = Course.objects.all()
    context = {'student': student, 'courses': courses}
    return render(request, 'teachers/edit_student.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_student(request, student_id):
    """Delete student"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    student = get_object_or_404(StudentProfile, user_id=student_id)
    user = student.user
    user.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('manage_students')


# ===== ATTENDANCE MANAGEMENT =====

@login_required(login_url='login')
def mark_attendance(request):
    """Mark attendance"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    selected_course_id = request.GET.get('course', '')

    if request.method == 'POST':
        date = request.POST.get('date')
        course_id = request.POST.get('course')
        students = StudentProfile.objects.filter(course_id=course_id)
        
        for student in students:
            is_present = request.POST.get(f'student_{student.user_id}') == 'on'
            Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'is_present': is_present}
            )
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('mark_attendance')

    courses = Course.objects.all()
    students = StudentProfile.objects.filter(course_id=selected_course_id) if selected_course_id else []
    context = {
        'courses': courses,
        'students': students,
        'selected_course_id': selected_course_id,
    }
    return render(request, 'teachers/mark_attendance.html', context)


@login_required(login_url='login')
def view_attendance(request):
    """View attendance records"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    attendance = Attendance.objects.all().select_related('student')
    context = {'attendance': attendance}
    return render(request, 'teachers/view_attendance.html', context)


# ===== RESULTS/MARKS MANAGEMENT =====

@login_required(login_url='login')
def add_marks(request):
    """Add marks to students"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        marks = request.POST.get('marks')
        remarks = request.POST.get('remarks', '')
        
        if not student_id or not subject_id or not marks:
            messages.error(request, 'Please fill all required fields!')
            return redirect('add_result')
        
        try:
            student = get_object_or_404(StudentProfile, user_id=student_id)
            
            subject = get_object_or_404(Subject, id=subject_id)
            
            Result.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': float(marks), 'remarks': remarks}
            )
            
            messages.success(request, f'Marks added successfully!')
            return redirect('add_result')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('add_result')
    
    students = StudentProfile.objects.all()
    subjects = Subject.objects.all()
    context = {'students': students, 'subjects': subjects}
    return render(request, 'teachers/add_marks.html', context)


@login_required(login_url='login')
def view_marks(request):
    """View all marks"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    results = Result.objects.all().select_related('student', 'subject')
    context = {'results': results}
    return render(request, 'teachers/view_marks.html', context)
