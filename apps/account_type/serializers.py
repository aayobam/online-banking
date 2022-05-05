from rest_framework import serializers
from apps.account_type.models import AccountType



class AccountTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountType
        fields = '__all__'
    
    def create(self, validated_data):
        account_type = AccountType.objects.create(**validated_data)
        return account_type

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(key, value, instance)
        instance.save()
        return instance