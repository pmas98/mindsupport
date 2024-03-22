from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from api.models import Usuario
class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows authentication using email.
    """

    def authenticate(self, request, email=None, password=None):
        try:
            user = Usuario.objects.get(email=email)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None