from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'is_pinned', 'is_active', 'publish_until', 'created_by', 'created_at')
    list_filter = ('audience', 'is_pinned', 'is_active')
    search_fields = ('title', 'message')
