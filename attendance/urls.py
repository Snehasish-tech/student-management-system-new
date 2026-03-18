from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.attendance_report, name='attendance_report'),
    path('my-attendance/', views.student_attendance_view, name='my_attendance'),
]
