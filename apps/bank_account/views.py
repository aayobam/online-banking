import random
from rest_framework import generics, status
from rest_framework.response import Response
from apps.bank_account.models import BankAccount
from apps.common import permission, custom_validator
from apps.bank_account.serializers import BankAccountVerifySerializer, BankAccountSerializer


class GetBankAccountNumberApiView(generics.CreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountVerifySerializer
    permission_classes = [permission.IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        payload = self.request.data
        file_obj = payload.get("identity_verification", None)
        custom_validator.file_validation(value=file_obj)
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user)
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
    lookup_url_kwarg = "account_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if response.data["verification_status"] == "pending":
            return Response("Your account is still pending verification")
        
        if response.data["verification_status"] == "failed":
            return Response("Your account verification has failed. Please re-upload a clear version of your document or visit the bank for assistance.")
        
        return Response(response.data, status=status.HTTP_200_OK)


class BankAccountUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwarg = "account_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def get_account_number(self):
        account_no = random.randrange(0000000000, 9999999999)
        return account_no

        

    def put(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)
        


class DeleteBankAccountApiView(generics.DestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwargs = "account_id"
    lookup_field = "id"