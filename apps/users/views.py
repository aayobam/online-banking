from apps.users.models import CustomUser
from rest_framework.response import Response
from apps.common import permission, custom_validator
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, serializers, permissions
from apps.users.serializers import (
    UserSerializer,
    UserRegisterationSerializer,
    RequestPasswordResetSerializer,
    CustomTokenObtainPairSerializer
    
)


class RegisterUserApiView(generics.CreateAPIView):
    """
    Register new users
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data.copy()
        email = payload.get("email", None)
        username = payload.get("username", None)
        birth_date = payload.get("birth_date", None)

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already exist in our database.")
        
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username already exist in our database.")

        age = custom_validator.verify_date_of_birth(value=birth_date)

        if age < 18:
            raise ValidationError(f"you are {age} years of age. you must be 18 years of age and above to own an account.")

        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(role="Customer", age=age)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class UserListApiView(generics.ListAPIView):
    """
    Only superuser can view lists of all users registered on
    the system.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permission.IsSuperUser]


class UserDetailApiView(generics.RetrieveAPIView):
    """
    Each user can view his/her detail but can't view other
    users account details.Only the superuser can view all users details.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated,permission.IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class UserUpdateApiView(generics.RetrieveUpdateAPIView):
    """
    Each user can edit/update his/her detail but can't edit/update other
    users account details. Only the superuser can edit/update all users details.
    """
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = "user_id"
    lookup_field = "id"
    permission_classes = [permission.IsSuperUser]
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)
    

class UserDeleteApiView(generics.RetrieveDestroyAPIView):
    """
    Each user can delete his/her detail but can't delete other
    users account details. Only the superuser can delete all users details.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"
    lookup_field = "id"
    permission_classes = [permission.IsSuperUser]


class RequestPasswordResetApiView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer
    def post(self, request):
        payload = {"request": request, "data": request.data.copy()}
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)