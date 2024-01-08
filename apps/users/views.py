from rest_framework import permissions, serializers, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.common import custom_validator, permission_helper
from apps.users.models import CustomUser
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    UserRegisterationSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    User Views
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterationSerializer
    permission_classes = [permissions.AllowAny]

    def createUsers(self, request, *args, **kwargs):
        payload = request.data.copy()

        if CustomUser.objects.filter(email=payload["email", None]).exists():
            raise serializers.ValidationError(
                "This email already exist in our database.")

        if CustomUser.objects.filter(username=payload["username", None]).exists():
            raise serializers.ValidationError(
                "This username already exist in our database.")

        age = custom_validator.verify_date_of_birth(value=payload["birth_date", None])

        if age < 18:
            raise ValidationError(
                f"you are {age} years of age. you must be 18 \
                years of age and above to own an account."
            )

        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(role="Customer", age=age)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_all_users(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_user_by_id(self):
        return super().get_object()

    def update_user_record(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete_user_record(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def send_reset_password(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def set_password(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):

    """
    Authenticates user to generate and get access token
    that can be use to grant users access using simplejwt.
    """

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CustomTokenObtainPairSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_201_CREATED)
