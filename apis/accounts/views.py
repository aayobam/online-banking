from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from apis.accounts.models import Account
from apis.common import permission_helper
from apis.accounts.serializers import AccountSerializer, VerifyAccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = "account_id"
    permission_classes = [permission_helper.IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer_class = VerifyAccountSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        serializer_class = AccountSerializer
        payload = self.queryset.order_by("-created_date")
        page = self.paginate_queryset(payload)
        if page is not None:
            serializers = serializer_class(data=page, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = serializer_class(data=payload)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        serializer_class = AccountSerializer
        payload = get_object_or_404(self.queryset, id=kwargs.get("account_id"))
        serializers = serializer_class(data=payload)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        payload = get_object_or_404(self.queryset, kwargs.get("account_id"))
        serializer = AccountSerializer(data=request.data, instance=payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        payload = get_object_or_404(self.queryset, kwargs.get("account_id"))
        serializer = AccountSerializer(data=request.data, instance=payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        payload = get_object_or_404(self.queryset, kwargs.get("account_id"))
        payload.delete()
        return Response({"message": f"account record with account no: {payload.account_no} deleted."}, status=status.HTTP_200_OK)
