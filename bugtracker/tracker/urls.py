"""
URL configuration for tracker application.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bug/<int:bug_id>/', views.bug_detail, name='bug_detail'),
    path('bug/create/', views.create_bug, name='create_bug'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
]