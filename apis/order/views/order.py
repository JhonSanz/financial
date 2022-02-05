
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apis.order.serializers.order import OrderSerializer, OrderCreateSerializer
from apps.order.models import Order
from apis.utils.paginator import CustomPagination


class OrderApi(viewsets.ModelViewSet):
    queryset = Order.objects
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filters = []
        if self.action in ["list"]:
            self.queryset = Order.objects.filter(owner=self.request.user)
        return self.queryset.filter(*filters)

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            self.serializer_class = OrderCreateSerializer
        return self.serializer_class
