from django.contrib import admin
from .models import TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'subject', 'experience')
    list_filter = ('subject', 'created_at')
    search_fields = ('user__username', 'employee_id', 'subject')
    readonly_fields = ('created_at', 'updated_at')
