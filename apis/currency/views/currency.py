
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, When, Case, F
from apis.currency.serializers.currency import CurrencySerializer
from apps.order.models import Order
from apis.utils.paginator import CustomPagination


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
        return self.queryset.filter()

    def get_serializer_class(self):
        if self.action in ["list"]:
            self.serializer_class = CurrencySerializer
        return self.serializer_class
