from rest_framework import serializers
from apis.common import custom_validator
from apis.users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "age",
            "phone_no",
            "profile_picture",
            "detail_url",
        ]

    def get_detail_url(self, obj):
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

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password",
            "phone_no",
            "country",
            "profile_picture",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        if CustomUser.objects.filter(email=validated_data["email", None]).exists():
            raise serializers.ValidationError(
                "This email already exist in our database.")

        age = custom_validator.verify_date_of_birth(
            value=validated_data["birth_date", None])

        if age < 18:
            raise ValidationError(
                f"you are {age} years of age. you must be 18 \
                years of age and above to own an account."
            )

        user = CustomUser.objects.create_user(**validated_data)
        user.age = age
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
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
        user = UserSerializer(self.user)
        data["user"] = user.data
        return data


class PasswordResetSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, required=True)
    confirm_password = serializers.CharField(min_length=8, required=True)

    class meta:
        fields = '__all__'


class SetPasswordSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(min_length=8, required=True)

    def validate_password(self, validated_data):
        password = validated_data.get("password", None)
        confirm_password = validated_data.pop("confirm_password", None)
        if password != confirm_password:
            raise ValidationError("Passwords do not match, please try again.")
        return password
