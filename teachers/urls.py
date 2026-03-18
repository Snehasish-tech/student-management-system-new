from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    
    # Student Management
    path('manage-students/', views.manage_students, name='manage_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    
    # Attendance
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('view-attendance/', views.view_attendance, name='view_attendance'),
    
    # Marks
    path('add-marks/', views.add_marks, name='add_marks'),
    path('view-marks/', views.view_marks, name='view_marks'),
]
