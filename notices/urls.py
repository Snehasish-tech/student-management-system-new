from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('create/', views.create_notice, name='create_notice'),
    path('<int:notice_id>/edit/', views.edit_notice, name='edit_notice'),
    path('<int:notice_id>/delete/', views.delete_notice, name='delete_notice'),
]
