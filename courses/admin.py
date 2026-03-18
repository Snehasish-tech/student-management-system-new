from django.contrib import admin
from .models import Course, Subject


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration_months', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')
