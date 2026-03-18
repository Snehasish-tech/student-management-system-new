from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present', 'created_at')
    list_filter = ('date', 'is_present', 'student__course')
    search_fields = ('student__user__username', 'student__roll_number')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
