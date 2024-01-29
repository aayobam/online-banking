import datetime
from rest_framework import serializers
from apis.authotps.models import AuthOtp
from apis.common import custom_validator
from apis.users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # detail_url = serializers.SerializerMethodField(source="get_detail_url")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "age",
            "phone_no",
            "profile_picture",
        ]

    # def get_detail_url(self, obj):
    #     return obj.get_absolute_url()


class UserRegisterationSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=120,
        min_length=8,
        write_only=True,
        help_text="must not be less than 8",
        style={"input_type": "password"},
        required=True,
    )
    confirm_password = serializers.CharField(
        max_length=120,
        min_length=8,
        write_only=True,
        help_text="must not be less than 8",
        style={"input_type": "password"},
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password",
            "confirm_password",
            "phone_no",
            "country",
            "profile_picture",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")

        if CustomUser.objects.filter(email=attrs.get("email", None)).exists():
            raise serializers.ValidationError(
                "This email already exist in our database.")

        if password != confirm_password:
            raise ValidationError("passwords do not match, please try again.")

        age = custom_validator.verify_date_of_birth(value=attrs.get("birth_date", None))

        if age < 18:
            raise ValidationError(
                f"you are {age} years of age. you must be 18 years of age and above to own an account.")

        user = CustomUser.objects.create_user(**attrs)
        user.age = age
        user.set_password(password)
        user.save()

        encryptedOtp = gene
        otpDict = {
            "user": user,
            "otp": encryptedOtp,
            "expiry": datetime.timedelta.min(10),
            "description": "fresh account email verification."
        }
        return user


class VerifyAccountSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = "__all__"

    def validate(self, attrs):
        otp = attrs.get("otp", None)
        email = attrs.get("email", None)

        otpObject = AuthOtp.objects.select_related("user").filter(otp=otp, user__email=email).first()
        userObj = CustomUser.objects.filter(email=email).first()

        if otpObject is not None:
            if otpObject.expiry <= timezone.now() and userObj is not None:
                userObj.is_active = True
                userObj.save()

            elif otpObject.expiry > timezone.now():
                raise ValidationError("Otp has expired, sign in to request for a new otp.")
        
        raise ValidationError("Invalid otp supplied, please try again.")


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = CustomUser.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    """ "
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
        user = UserSerializer(self.user).data
        data["user"] = user
        return data


class PasswordResetSerializer(serializers.Serializer):

    password = serializers.CharField(min_length=8, required=True)

    confirm_password = serializers.CharField(min_length=8, required=True)

    class Meta:

        fields = ['password', 'confirm_password']

        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True}
        }


class SetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=8, required=True)

    class Meta:
        fields = "__all__"

    def validate_password(self, validated_data):
        password = validated_data.get("password", None)
        confirm_password = validated_data.pop("confirm_password", None)
        if password != confirm_password:
            raise ValidationError("Passwords do not match, please try again.")
        return password
