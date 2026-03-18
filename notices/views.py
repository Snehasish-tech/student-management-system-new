from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.utils.timezone import now

from .forms import NoticeForm
from .models import Notice


@login_required(login_url='login')
def notice_list(request):
    query = request.GET.get('q', '').strip()

    notices = Notice.objects.filter(is_active=True).order_by('-is_pinned', '-created_at')
    notices = notices.filter(Q(publish_until__isnull=True) | Q(publish_until__gte=now().date()))

    if request.user.is_student():
        notices = notices.filter(audience__in=['all', 'students'])
    elif request.user.is_teacher():
        notices = notices.filter(audience__in=['all', 'teachers', 'students'])

    if query:
        notices = notices.filter(Q(title__icontains=query) | Q(message__icontains=query))

    context = {
        'notices': notices,
        'query': query,
    }
    return render(request, 'notices/list.html', context)


@login_required(login_url='login')
def create_notice(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden('You are not authorized to access this page.')

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            messages.success(request, 'Notice published successfully.')
            return redirect('notice_list')
    else:
        form = NoticeForm(initial={'is_active': True})

    return render(request, 'notices/form.html', {'form': form, 'is_edit': False})


@login_required(login_url='login')
def edit_notice(request, notice_id):
    if not request.user.is_teacher():
        return HttpResponseForbidden('You are not authorized to access this page.')

    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'notices/form.html', {'form': form, 'is_edit': True, 'notice': notice})


@login_required(login_url='login')
def delete_notice(request, notice_id):
    if not request.user.is_teacher():
        return HttpResponseForbidden('You are not authorized to access this page.')

    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
    return redirect('notice_list')
