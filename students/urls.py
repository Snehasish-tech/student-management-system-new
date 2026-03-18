from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('results/', views.student_results, name='student_results'),
]
