from django.db.utils import OperationalError, ProgrammingError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.apps import apps

def create_group_permissions():
    try:
        Bug = apps.get_model('tracker', 'Bug')
        Project = apps.get_model('tracker', 'Project')
        Comment = apps.get_model('tracker', 'Comment')

        models_permissions = {
            'Developer': {
                Bug: ['view', 'change'],
                Comment: ['view', 'add'],
                Project: ['view'],
            },
            'Tester': {
                Bug: ['view', 'add'],
                Comment: ['view', 'add'],
                Project: ['view'],
            }
        }

        for role, perms in models_permissions.items():
            group, _ = Group.objects.get_or_create(name=role)

            for model, actions in perms.items():
                ctype = ContentType.objects.get_for_model(model)
                for action in actions:
                    codename = f"{action}_{model._meta.model_name}"
                    try:
                        perm = Permission.objects.get(codename=codename, content_type=ctype)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        print(f"Permission {codename} not found.")

    except (OperationalError, ProgrammingError):
        pass
