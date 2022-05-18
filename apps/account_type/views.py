from rest_framework import status, generics
from rest_framework.response import Response
from apps.account_type.models import AccountType
from apps.common import permission
from apps.account_type.serializers import AccountTypeSerializer


class CreateAccountTypeApiView(generics.CreateAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permission.IsSuperUser]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)


class AccountTypeListApiView(generics.ListAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permission.IsSuperUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class AccountTypeDetailApiView(generics.RetrieveAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permission.IsSuperUser]
    lookup_url_kwarg = "type_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class AccountTypeUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permission.IsSuperUser]
    lookup_url_kwarg = "type_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class AccountTypeDeleteApiView(generics.RetrieveDestroyAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permission.IsSuperUser]
    lookup_url_kwarg = "type_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)