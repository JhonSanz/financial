
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, When, Case, F
from apis.currency.serializers.currency import (
    CurrencySerializer, CurrencyAllSerializer)
from apps.order.models import Order
from apis.utils.paginator import CustomPagination
from apis.utils.currency_list import get_currencies


class CurrencyApi(viewsets.ModelViewSet):
    queryset = Order.objects
    serializer_class = CurrencySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action in ["list"]:
            self.queryset = (
                Order.objects
                .filter(owner=self.request.user)
                .annotate(
                    negative=Case(
                        When(type=0, then=F('amount_currency') * -1),
                        default=F('amount_currency')
                    )
                )
                .values('currency')
                .annotate(amount=Sum('negative'))
                .order_by('-amount')
            )
        if self.action in ['all']:
            self.queryset = Order.objects.values('currency').distinct()
        return self.queryset.filter()

    def get_serializer_class(self):
        if self.action in ["list"]:
            self.serializer_class = CurrencySerializer
        if self.action in ["all"]:
            self.serializer_class = CurrencyAllSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def all(self, request):
        serializer = self.get_serializer_class()
        data = serializer(
            self.get_queryset(),
            many=True
        ).data
        return Response({'data': data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def gecko_coins(self, request):
        return Response({'data': get_currencies()}, status=status.HTTP_200_OK)
