"""
URL configuration for tracker application.
"""

from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .forms import LoginForm

urlpatterns = [
    path('accounts/login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=LoginForm,
    ), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('bug/<int:bug_id>/', views.bug_detail, name='bug_detail'),
    path('project/<int:project_id>/', views.project_view, name='project_view'),
    path('bug/create/', views.create_bug, name='create_bug'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('accounts/register/', views.register, name='register'),
]