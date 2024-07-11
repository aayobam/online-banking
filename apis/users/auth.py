from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from apis.users.utils import get_user_session_key
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme


class CustomJwtAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        if token.get('session_id') != get_user_session_key(token.get('user_id')):
            raise AuthenticationFailed("Invalid Session", code=401)
        return token

    def authenticate(self, request: Request):
        header = self.get_header(request)

        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    target_class = CustomJwtAuthentication
