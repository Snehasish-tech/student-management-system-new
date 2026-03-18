from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Result
from .forms import ResultForm
from students.models import StudentProfile
from courses.models import Subject


@login_required(login_url='login')
def teacher_results(request):
    """List all results for teacher"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    results = Result.objects.all().select_related('student', 'subject')
    context = {'results': results}
    return render(request, 'marks/teacher_results.html', context)


@login_required(login_url='login')
def add_result(request):
    """Add result for student"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully!')
            return redirect('teacher_results')
    else:
        form = ResultForm()
    
    context = {'form': form}
    return render(request, 'marks/add_result.html', context)


@login_required(login_url='login')
def edit_result(request, result_id):
    """Edit result"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    result = get_object_or_404(Result, id=result_id)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result updated successfully!')
            return redirect('teacher_results')
    else:
        form = ResultForm(instance=result)
    
    context = {'form': form, 'result': result}
    return render(request, 'marks/edit_result.html', context)


@login_required(login_url='login')
def delete_result(request, result_id):
    """Delete result"""
    if not request.user.is_teacher():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    result = get_object_or_404(Result, id=result_id)
    result.delete()
    messages.success(request, 'Result deleted successfully!')
    return redirect('teacher_results')


@login_required(login_url='login')
def student_results(request):
    """Student view their results"""
    if not request.user.is_student():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    try:
        student = StudentProfile.objects.get(user=request.user)
        results = Result.objects.filter(student=student).select_related('subject')
        
        # Calculate overall statistics
        total_marks = sum([r.marks for r in results]) if results else 0
        avg_marks = total_marks / len(results) if results else 0
        
        context = {
            'results': results,
            'total_marks': total_marks,
            'avg_marks': round(avg_marks, 2),
            'total_subjects': len(results),
        }
        return render(request, 'marks/student_results.html', context)
    except StudentProfile.DoesNotExist:
        return HttpResponseForbidden("Student profile not found.")
