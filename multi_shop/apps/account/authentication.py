from django.contrib.auth.backends import BaseBackend
from . import models


class EmailAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = models.User.objects.get(email=username)
            if user and user.check_password(password):
                return user
            return None
        except :
            return None

    def get_user(self, user_id):
        try:
            return models.User.objects.get(id=user_id)
        except :
            return None