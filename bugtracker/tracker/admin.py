from django.contrib import admin
from .models import Project, Bug, Comment

admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(Comment)