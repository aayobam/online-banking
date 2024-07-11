from django.shortcuts import get_object_or_404
from apis.common.custom_generators import account_verification_otp_generator
from apis.users.tasks import send_password_reset_mail
from apis.users.utils import delete_user_session
from core import settings
from rest_framework import permissions, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from apis.users.models import CustomUser, Token
from apis.users import serializers
from core import tasks
from django.db import transaction
from django.utils.crypto import get_random_string


class UserViewSet(viewsets.GenericViewSet, generics.ListAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_url_kwarg = "user_id"

    def get_serializer_class(self):
        if self.action == "create_user":
            return serializers.UserRegisterationSerializer
        elif self.action == "all_users":
            return serializers.UserSerializer
        elif self.action == "initiate_password_reset":
            return serializers.InitiatePasswordResetSerializer
        elif self.action == "set_new_password":
            return serializers.SetPasswordSerializer
        elif self.action in ['update_user', 'partial_update_user']:
            return serializers.UserSerializer
        elif self.action == "verify_account":
            return serializers.VerifyAccountSerializer
        return super().get_serializer_class()
    
    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action in ["create", "initialize_reset", "set_new_password"]:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()  

    @action(detail=False, methods=["POST"], url_name="create-user-account")
    def create_user(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.get_serializer_class(payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(role="Customer")

        # user = serializer.data.copy()
        # otp_user_object = account_verification_otp_generator(user)
        # message = f"""Your One Time Password(OTP) for swift bank account verification is { otp_user_object.otp}.
        # Note: Otp expires in 10 minutes."""
        # tasks.send_verification_otp_mail_task.delay(
        #     subject="Verify your Account.",
        #     message=message,
        #     receiver_email=user.email,
        #     sender_email=base.SENDER_EMAIL
        # )
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"], url_name="verify-account")
    def verify_account(self, request, *args, **kwargs):
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
            sender_email=settings.SENDER_EMAIL
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["GET"], url_name="get-all-users")
    def all_users(self, request, *args, **kwargs):
        payloads = self.queryset.order_by("-date_created")
        page = self.paginate_queryset(payloads)
        if page is not None:
            serializers = self.get_serializer_class(page, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = self.get_serializer_class(payloads, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_name="get-user-detail")
    def user_detail(self, request, *args, **kwargs):
        payload = self.get_object()
        serializer = self.get_serializer_class(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"], url_name="update-user-detail")
    def update_user(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer_class(data=request.data, instance=queryset)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_name="partial-update-user-detail")
    def partial_update_user(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer_class(data=request.data, instance=queryset, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"], url_name="delete-user-account")
    def delete_user(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response("User deleted successfully.", status=status.HTTP_200_OK)
    
    @transaction.atomic
    @action(methods=["POST"], detail=False, url_path="reset-password")
    def initiate_password_reset(self, request, id=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message = "The password reset link you received confirms that we have received your request. " \
                      "Confirm that you are resetting your password by clicking on the 'RESET MY PASSWORD' button"
            email = request.data["email"].lower().strip()
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({"success": True, "message": "Email successfully sent to registered email"}, status=status.HTTP_200_OK)
            token_obj, created = Token.objects.update_or_create(
                user=user,
                token_type="PASSWORD_RESET",
                defaults={"user": user, "token_type": "PASSWORD_RESET", "token": get_random_string(120)}
            )
            user_data = {
                "email": user.email,
                "fullname": f"{user.get_full_name()}",
                "password_reset_url": f"{self.request.scheme}://{self.request.get_host()}/set-new-password/?token={token_obj.token}",
                "message": message,
                "email_subject": "Password Reset",
            }
            send_password_reset_mail.delay(user_data, "Password Reset")
            return Response({"success": True, "message": "Email successfully sent to registered email"}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(methods=["POST"], detail=False,  url_path="set-new-password", lookup_url_kwarg="token")
    def set_new_password(self, request, token=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token_obj = Token.objects.filter(token=request.data["token"]).first()
            if not token_obj or not token_obj.is_valid():
                return Response({"success": False, "detail": "Invalid token specified"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(CustomUser, id=token_obj.user.id)
            if not user:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            password = serializer.validated_data.get("new_password", None)
            confirm_password = serializer.validated_data.get("confirm_password", None)
            if confirm_password != password:
                raise serializers.ValidationError({"message": "passwords do not match."})
            
            token_obj.reset_user_password(password)
            token_obj.verify_user()
            token_obj.delete()
            return Response({"success": True, "message": "Password has been created successfully"}, status=status.HTTP_200_OK,)
        return Response({"success": False, "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class CustomObtainTokenPairView(TokenObtainPairView):
    """Login with email and password"""

    serializer_class = serializers.CustomObtainTokenPairSerializer


class LogoutView(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserLogoutSerializer

    @action(methods=["POST"], detail=False, url_path="logout")
    def logout_session(self, request):
        delete_user_session(request.user.id)
        return Response({"success": True, "message": "User logged out successfully"}, status=status.HTTP_200_OK)