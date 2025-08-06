from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BugForm, CommentForm, ProjectForm
from .models import Bug, Project


@login_required
def dashboard(request):
    bugs = Bug.objects.all().order_by('-created_at')
    return render(request, 'tracker/dashboard.html', {'bugs': bugs})


@login_required
def bug_detail(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)
    comments = bug.comment_set.all().order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.bug = bug
            comment.user = request.user
            comment.save()
            return redirect('bug_detail', bug_id=bug.id)
    else:
        form = CommentForm()

    context = {
        'bug': bug,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'tracker/bug_detail.html', context)

@login_required
def create_bug(request):
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.created_by = request.user
            bug.save()
            return redirect('dashboard')
    else:
        form = BugForm()
    return render(request, 'tracker/bug_form.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'tracker/project_form.html', {'form': form})
