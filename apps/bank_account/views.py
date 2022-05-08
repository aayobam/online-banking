from random import randint
from apps.common import custom_validator
from rest_framework.exceptions import ValidationError
from apps.common import permission
from rest_framework import generics, status
from rest_framework.response import Response
from apps.bank_account.models import BankAccount
from apps.bank_account.serializers import BankAccountSerializer


class GetBankAccountNumberApiView(generics.CreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def post(self, request, *args, **kwargs):
        payload = self.request.data
        file_obj = payload.get("identity_verification", None)
        birth_date_obj = payload.get("birth_date", None)
        custom_validator.file_validation(value=file_obj)
        custom_validator.verify_date_of_birth(value=birth_date_obj)
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BankAccountListApiView(generics.ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class BankccountDetailApiView(generics.RetrieveAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwargs = "account_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if response.data["verification_status"] == "Pending":
            return Response("Your account is still pending verification")
        
        if response.data["verification_status"] == "Failed":
            return Response("Your account is verification has failed. Please re-upload a clear version of your document or visit the bank for assistance.")
        return Response(response.data, status=status.HTTP_200_OK)


class BankAccountUpdateApiView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwargs = "account_id"
    lookup_field = "id"

    def generate_account_number(self):
        return randint(1000000000, 9999999999)

    def put(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.data["verification_status"] == "Pending" or response.data["verification_status"] == "Failed":
            response.data["account_number"] = None
        response.data["account_number"] = self.generate_account_number()
        return Response(response.data, status=status.HTTP_200_OK)


class DeleteBankAccountApiView(generics.DestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwargs = "account_id"
    lookup_field = "id"