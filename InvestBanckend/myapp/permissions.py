from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        
        if auth_header is not None:
            try:
                token = auth_header.split(' ')[1]
                AccessToken(token)  # Validate the token
                return True
            except Exception as e:
                raise AuthenticationFailed('Invalid or expired token')
        return False
