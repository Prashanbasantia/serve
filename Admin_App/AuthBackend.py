from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class Login(ModelBackend):
    def authenticate(self,email=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(Q(email=email) | Q(phone = email))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None