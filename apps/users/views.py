from rest_framework import permissions, serializers, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.common import custom_validator, permission_helper
from apps.users.models import CustomUser
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
    SetPasswordSerializer,
    UserRegisterationSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    User Views
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterationSerializer
    permission_classes = []

    @action(detail=True, methods=["POST"])
    def create_users(self, request, *args, **kwargs):
        payload = request.data.copy()

        if CustomUser.objects.filter(email=payload["email", None]).exists():
            raise serializers.ValidationError("This email already exist in our database.")

        if CustomUser.objects.filter(username=payload["username", None]).exists():
            raise serializers.ValidationError("This username already exist in our database.")

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

    @action(detail=True, methods=["GET"])
    def get_all_users(self, request, *args, **kwargs):
        payloads = self.queryset.all()
        serializers = self.serializer_class(data=payloads, many=True)
        if serializers.data == []:
            return Response({"message": "You don't have ."}, status=status.HTTP_200_OK)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def get_user_by_detail(self, id=None):
        self.permission_classes.append("IsAuthenticated")
        payload = self.queryset.filter(id=id).first()
        serializer = self.serializer_class(data=payload)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT", "PATCH"])
    def update_user_record(self, request, *args, **kwargs):
        payload = self.queryset.filter(id=kwargs["id"]).first()
        serializers = self.serializer_class(data=payload)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"])
    def delete_user_record(self, request, *args, **kwargs):
        payload = self.queryset.filter(id=kwargs["id"]).first()
        serializers = self.serializer_class(data=payload)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def reset_password(self, request, *args, **kwargs):
        serializer_class = PasswordResetSerializer
        payload = request.data.copy()
        serializers = serializer_class(data=payload)
        serializers.is_valid(raise_exception=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def set_password(self, request):
        user = self.get_object()
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response("password set", status=status.HTTP_200_OK)


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
