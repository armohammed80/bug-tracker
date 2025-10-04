from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        try:
            # Check user with the same username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                # Check user with the same email
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return

        # Check password
        if user.check_password(password):
            return user
