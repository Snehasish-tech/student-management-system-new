from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'college_id', 'course')
    list_filter = ('course', 'created_at')
    search_fields = ('user__username', 'roll_number', 'college_id')
    readonly_fields = ('created_at', 'updated_at')
