from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Course, Subject
from .forms import CourseForm, SubjectForm


@login_required(login_url='login')
def list_courses(request):
    """List all courses"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/list.html', context)


@login_required(login_url='login')
def add_course(request):
    """Add new course"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('list_courses')
    else:
        form = CourseForm()
    
    context = {'form': form}
    return render(request, 'courses/form.html', context)


@login_required(login_url='login')
def edit_course(request, course_id):
    """Edit course"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('list_courses')
    else:
        form = CourseForm(instance=course)
    
    context = {'form': form, 'course': course}
    return render(request, 'courses/form.html', context)


@login_required(login_url='login')
def delete_course(request, course_id):
    """Delete course"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('list_courses')


# Subject Views
@login_required(login_url='login')
def list_subjects(request):
    """List all subjects"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request, 'courses/subjects_list.html', context)


@login_required(login_url='login')
def add_subject(request):
    """Add new subject"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('list_subjects')
    else:
        form = SubjectForm()
    
    context = {'form': form}
    return render(request, 'courses/subject_form.html', context)


@login_required(login_url='login')
def edit_subject(request, subject_id):
    """Edit subject"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('list_subjects')
    else:
        form = SubjectForm(instance=subject)
    
    context = {'form': form, 'subject': subject}
    return render(request, 'courses/subject_form.html', context)


@login_required(login_url='login')
def delete_subject(request, subject_id):
    """Delete subject"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject deleted successfully!')
    return redirect('list_subjects')
