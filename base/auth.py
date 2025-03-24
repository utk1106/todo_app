# base/auth.py
from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

class JWTBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        return None  # We don't use this for direct authentication

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.session.get('access_token')
        if access_token:
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(access_token)
                request.user = jwt_auth.get_user(validated_token)
            except Exception:
                request.user = None
        return self.get_response(request)