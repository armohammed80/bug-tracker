from .forms import BugForm, CommentForm, ProjectForm, CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from .models import Bug, Project, Organization, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User


User = get_user_model()

@login_required
def dashboard(request):
    try:
        user_org = request.user.userprofile.organization
    except UserProfile.DoesNotExist:
        logout(request)
        return redirect('register')

    bugs = Bug.objects.filter(organization=user_org).order_by('-created_at')
    return render(request, 'tracker/dashboard.html', {'bugs': bugs})


@login_required
def bug_detail(request, bug_id):
    user_org = request.user.userprofile.organization
    bug = get_object_or_404(Bug, id=bug_id, organization=user_org)
    comments = bug.comment_set.all().order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if 'status' in request.POST:
            new_status = request.POST['status']
            if new_status in dict(Bug.STATUS_CHOICES):
                bug.status = new_status
                bug.save()
                return redirect('bug_detail', bug_id=bug.id)
        if 'assigned_to' in request.POST:
            if assigned_person := request.POST['assigned_to']:
                bug.assigned_to = get_object_or_404(User, id=assigned_person, userprofile__organization=bug.organization)
                bug.save()
                return redirect('bug_detail', bug_id=bug.id)
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
        'status_choices': Bug.STATUS_CHOICES,
        'users': User.objects.filter(userprofile__organization=bug.organization),
    }
    return render(request, 'tracker/bug_detail.html', context)

@login_required
def project_view(request, project_id):
    user_org = request.user.userprofile.organization
    project = get_object_or_404(Project, id=project_id, organization=user_org)
    bugs = Bug.objects.filter(project=project, organization=user_org).order_by('-created_at')
    return render(request, 'tracker/project_detail.html', {
        'project': project,
        'bugs': bugs
    })

@login_required
def create_bug(request):
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.organization = request.user.userprofile.organization
            bug.created_by = request.user
            bug.save()
            return redirect('dashboard')
    else:
        form = BugForm()
    return render(request, 'tracker/bug_form.html', {'form': form})

@login_required
def project_list(request):
    user_org = request.user.userprofile.organization
    projects = Project.objects.filter(organization=user_org)
    return render(request, 'tracker/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.organization = request.user.userprofile.organization
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'tracker/project_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        role = request.POST.get('role')
        org_choice = request.POST.get('org_choice')
        new_org_name = request.POST.get('new_org')

        if form.is_valid() and role:
            user = form.save(commit=False)

            if new_org_name:
                organization, _ = Organization.objects.get_or_create(name=new_org_name.strip())
            elif org_choice:
                try:
                    organization = Organization.objects.get(id=org_choice)
                except Organization.DoesNotExist:
                    form.add_error(None, "Selected organization does not exist.")
                    organizations = Organization.objects.all()
                    return render(request, 'registration/register.html', {
                        'form': form,
                        'organizations': organizations
                    })
            else:
                form.add_error(None, "You must either join or create an organization.")
                organizations = Organization.objects.all()
                return render(request, 'registration/register.html', {
                    'form': form,
                    'organizations': organizations
                })

            # Set the required organization
            user.organization = organization
            user.save()

            UserProfile.objects.create(user=user, organization=organization)

            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Group.DoesNotExist:
                form.add_error(None, "Invalid role selected.")
                organizations = Organization.objects.all()
                return render(request, 'registration/register.html', {
                    'form': form,
                    'organizations': organizations
                })

            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    organizations = Organization.objects.all()
    return render(request, 'registration/register.html', {
        'form': form,
        'organizations': organizations
    })
