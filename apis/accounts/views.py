from rest_framework import generics, status
from rest_framework.response import Response
from apis.accounts.models import Account
from apis.common import permission_helper
from apis.accounts.serializers import AccountSerializer, VerifyAccountSerializer


class GetAccountNumberApiView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = VerifyAccountSerializer
    permission_classes = [permission_helper.IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountListApiView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class AccountDetailApiView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = "account_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if response.data["verification_status"] == "pending":
            return Response("Your account is still pending verification.")

        if response.data["verification_status"] == "failed":
            return Response("Your account verification has failed.Retry again.")

        return Response(response.data, status=status.HTTP_200_OK)


class AccountUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = "account_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class DeleteAccountApiView(generics.DestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwargs = "account_id"
    lookup_field = "id"
