from rest_framework import serializers

from apis.accounts.models import Account


class VerifyAccountSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.get_full_name")
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        bank_account = Account.objects.create(**validated_data)
        return bank_account

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def get_detail_url(self, obj):
        return obj.get_absolute_url()


class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.get_full_name")

    class Meta:
        model = Account
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        bank_account = Account.objects.create(**validated_data)
        return bank_account
