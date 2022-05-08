from rest_framework import serializers
from apps.bank_account.models import BankAccount



class BankAccountSerializer(serializers.ModelSerializer):
    identity_verification = serializers.FileField(required=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = ['account_type', 'identity_verification', 'detail_url']
    
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
            