from apis.common.custom_generators import account_verification_otp_generator
from core.settings import base
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from apis.common import permission_helper
from apis.users.models import CustomUser
from apis.users import serializers
from core import tasks


class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_url_kwarg = "user_id"

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserRegisterationSerializer
        elif self.action == "reset_password":
            return serializers.PasswordResetSerializer
        elif self.action == "set_password":
            return serializers.SetPasswordSerializer
        elif self.action == "verify_account":
            return serializers.VerifyAccountSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Create new user.
        """

        payload = request.data
        serializer = self.get_serializer_class(payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(role="Customer")

        user = serializer.data.copy()
        otp_user_object = account_verification_otp_generator(user)
        message = f"""Your One Time Password(OTP) for swift bank account verification is { otp_user_object.otp}.
        Note: Otp expires in 10 minutes."""
        tasks.send_verification_otp_mail_task.delay(
            subject="Verify your Account.",
            message=message,
            receiver_email=user.email,
            sender_email=base.DEFAULT_FROM_EMAIL
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def verify_account(self, request, *args, **kwargs):
        """
        Create new user.
        """

        payload = request.data
        serializer = self.get_serializer_class(payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(role="Customer")

        user = serializer.data
        otp_object = account_verification_otp_generator(user)
        message = f"your account verification code is {otp_object.code}"
        tasks.send_verification_otp_mail_task.delay(
            subject="Activate your Account.",
            message=message,
            receiver_email=user.email,
            sender_email=base.DEFAULT_FROM_EMAIL
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([permissions.IsAuthenticated])
    def list(self, request, *args, **kwargs):
        """
        Fetch all user records.
        """
        payloads = self.queryset.order_by("-date_created")
        page = self.paginate_queryset(payloads)
        if page is not None:
            serializers = self.get_serializer_class(page, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = self.get_serializer_class(payloads, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve user detail.
        """
        payload = self.get_object()
        serializer = self.get_serializer_class(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Update user detail.
        """
        queryset = self.get_object()
        serializer = self.get_serializer_class(data=request.data, instance=queryset)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update user record.
        """
        queryset = self.get_object()
        serializer = self.get_serializer_class(
            data=request.data, instance=queryset, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def destroy(self, request, *args, **kwargs):
        """
        Delete user record.
        """
        instance = self.get_object()
        instance.delete()
        return Response("User deleted successfully.", status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    @permission_classes([permissions.AllowAny])
    def reset_password(self, request):
        """
        provide email for password reset.
        """
        payload = request.data
        serializer = self.get_serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        otp_user_object = account_verification_otp_generator(user)
        message = f"""Your One Time Password(OTP) for swift bank password reset is { otp_user_object.otp}.
        Note: Otp expires in 10 minutes."""

        tasks.send_password_reset_token_task.delay(
            subject="Password Reset Request.",
            message=message,
            receiver_email=serializer.data.email,
            sender_email=base.DEFAULT_FROM_EMAIL
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    @permission_classes([permissions.AllowAny])
    def set_password(self, request):
        """
        set new password. both password and confirm_password fields must match.
        """
        user = self.get_object()
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        message = f"Your password reset request complete."

        tasks.send_password_reset_token_task.delay(
            subject="Password Reset Complete.",
            message=message,
            receiver_email=serializer.data.email,
            sender_email=base.DEFAULT_FROM_EMAIL
        )

        return Response("Password set successfully.", status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):

    """
    Authenticates user to generate and get access token
    that can be use to grant users access using simplejwt.
    """

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = serializers.CustomTokenObtainPairSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
