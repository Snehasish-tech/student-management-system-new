from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'grade', 'created_at')
    list_filter = ('grade', 'subject__course', 'created_at')
    search_fields = ('student__user__username', 'subject__name')
    readonly_fields = ('grade', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        obj.save()
