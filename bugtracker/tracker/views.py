from django.shortcuts import render
from .models import Bug
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    bugs = Bug.objects.all()
    return render(request, 'tracker/dashboard.html', {'bugs': bugs})