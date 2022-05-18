from textwrap import indent
from rest_framework import serializers
from apps.bank_account.models import BankAccount



class BankAccountVerifySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.get_full_name')
    verification_status = serializers.ReadOnlyField()
    account_no = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()
    transfer_limit = serializers.ReadOnlyField()
    verification_status = serializers.ReadOnlyField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = '__all__'
    
    def create(self, validated_data):
        bank_account = BankAccount.objects.create(**validated_data)
        return bank_account

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def get_detail_url(self, obj):
        return obj.get_absolute_url()


class BankAccountSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.get_full_name')
    identity_verification = serializers.FileField(required=False)
    class Meta:
        model = BankAccount
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        bank_account = BankAccount.objects.create(**validated_data)
        return bank_account