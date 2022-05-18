from django.urls import reverse
from rest_framework import serializers
from apps.users.models import CustomUser
from core.settings import DEFAULT_FROM_EMAIL
from apps.common.email import EmailNotification
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError




class UserSerializer(serializers.ModelSerializer):

    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", 'username', 'email', 'first_name', 'last_name','birth_date', 'age', 'phone_no', 'profile_picture', 'detail_url']

    def get_detail_url(self, obj):
        return obj.get_absolute_url()
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserRegisterationSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=120, 
        min_length=8, 
        write_only=True, 
        help_text="must not be less than 8", 
        style={'input_type':"password"},
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "first_name", "last_name", "birth_date", "age", "password", "phone_no", "country", "profile_picture", "detail_url"]
        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for (key, value) in validated_data.items():
            setattr(key, value, instance)
        
        if password is None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_detail_url(self, obj):
        return obj.get_absolute_url()


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = CustomUser.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    """"
    Generates refresh token for users and returns new access token
    """
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        user = UserSerializer(self.user)
        data["user"] = user.data
        return data


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email',]

    def validate(self, attrs):
        try:
            email = attrs["data"].get('email', None)
            request = attrs["data"].get("request", None)
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request).domain
                relativelink = reverse("reser-password")
                absurl = 'http://'+current_site+relativelink+"?token="+str(token)
                email_body = f"Hello {user.get_full_name}, use the link below to reset your password\n{absurl}"
                data = {
                    "email_subject": "Reset your password",
                    "email_body": email_body,
                    "to_email": user.email,
                }
                mailer = EmailNotification(
                    subject=data["email_subject"],
                    message=data["email_body"],
                    sender_email=DEFAULT_FROM_EMAIL,
                    receiver_email=data["to_email"]
                )
                mailer.registeration_email()
            return attrs
        except:
            pass
        return super().validate(attrs)