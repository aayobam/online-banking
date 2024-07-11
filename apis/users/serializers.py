import datetime
import secrets
from rest_framework import serializers
from apis.accounts.models import Account
from apis.authotps.models import AuthOtp
from django.utils.translation import gettext_lazy as _
from apis.users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from apis.users.utils import get_or_create_user_session_key
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.SerializerMethodField(source="get_detail_url")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "age",
            "phone_no",
            "profile_picture",
            "detail_url"
        ]

    async def get_detail_url(self, obj):
        return obj.get_absolute_url()


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
            "date_of_birth",
            "password",
            "confirm_password",
            "phone_no",
            "country",
            "profile_picture",
        ]
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}, "confirm_password": {"write_only": True}}

    async def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        confirm_password = attrs.pop("confirm_password", None)
        date_of_birth = attrs.get("birth_date", None)

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "This email already exist in our database."})
        if password != confirm_password:
            raise serializers.ValidationError({"messages": "passwords do not match, please try again."})
        age = self.verify_date_of_birth(value=date_of_birth)
        if age < 18:
            raise serializers.ValidationError({"message": "you are {age} years of age. you must be 18 years of age and above to own an account."})
        if age > 1000:
            raise serializers.ValidationError({"message": f"age cannot be more than {1000} years old"})
        attrs["age"] = age
        return attrs
    
    @transaction.atomic
    async def create(self, validated_data):
        password = validated_data.get("password")
        account_type = validated_data.get("account_type")
        user = await CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        account_number = await self.generate_account_no()
        daily_transfer_limit = await self.generate_daily_transfer_limit(account_type)
        
        account = await Account.objects.create(
            owner=user,
            account_type=account_type,
            account_no=account_number,
            balance=0.00,
            daily_transfer_limit=daily_transfer_limit,
            verification_status="Verified"
        )
        account.save()
        return user

    @staticmethod
    async def verify_date_of_birth(date_of_birth):
        today = datetime.date.today()
        age = today.year - date_of_birth.year
        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
            age -= 1
        return age
    
    @staticmethod
    async def generate_account_no():
        account_no = secrets.randbelow(10**10)
        return account_no
    
    @staticmethod
    async def generate_daily_transfer_limit(account_type):
        if account_type == "Savings":
            return 1000000.00       
        elif account_type == "Current":
            return 5000000.00
        else:
            return 0.00
        
        
    

class VerifyAccountSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = "__all__"

    async def validate(self, attrs):
        otp = attrs.get("otp", None)
        email = attrs.get("email", None)
        user_otp = await AuthOtp.objects.select_related("user").filter(otp=otp, user__email=email).first()
        if user_otp is not None:
            user = user_otp.user
            if user_otp.expiry <= timezone.now() and user is not None:
                user.is_active = True
                user.save()
            elif user_otp.expiry > timezone.now():
                raise serializers.ValidationError({"message": "Otp has expired, sign in to request for a new otp."})
        raise serializers.ValidationError({"message": "Invalid otp supplied, please try again."})


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {"email": _("Invalid email or password")}

    @classmethod
    async def get_token(cls, user):
        if not user.is_active:
            raise AuthenticationFailed(_("Account not active."), code="authentication")
        token = super().get_token(user)
        token["user"] = UserSerializer(user).data
        token['session_id'] = get_or_create_user_session_key(str(user.id))
        user.save()
        return token


class InitiatePasswordResetSerializer(serializers.Serializer):
    """Serializer for sending password reset email to the user"""

    email = serializers.CharField(required=True)

    async def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get("email", None)
        if not await CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "email supplied does not exist."})
        return attrs


class SetPasswordSerializer(serializers.Serializer):
    """Serializer for password change on reset"""

    token = serializers.CharField(required=True)
    new_password = serializers.RegexField(regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', write_only=True, error_messages={
                                          'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirm_password = serializers.CharField(write_only=True, required=True)


class UserLogoutSerializer(serializers.Serializer):
    pass
    # id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), read_only=True)
