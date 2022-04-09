import json
from django.db.models import Q, Sum, When, Case, F
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser
from apis.order.serializers.order import (
    OrderSerializer, OrderCreateSerializer,
    OrderPositionsSerializer
)
from apps.order.models import Order
from apis.utils.paginator import CustomPagination
from apis.order.utils.excel_file import FileReader
from apis.utils.currency_name_from_object import convert_object_to_name


class OrderApi(viewsets.ModelViewSet):
    queryset = Order.objects
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    parser_class = (MultiPartParser, JSONParser)

    def get_queryset(self):
        filters = [Q(owner=self.request.user)]
        if self.action in ["list"]:
            self.queryset = Order.objects
        if self.action in ["position"]:
            filters.append(Q(type=Order.BUY))
            if "currency" in self.request.GET:
                currency = convert_object_to_name(
                    json.loads(self.request.GET["currency"]))
                filters.append(Q(currency=currency))
            if "open" in self.request.GET:
                subquery = (
                    Order.negative_columns
                    .negative_values()
                    .values('position', 'currency')
                    .annotate(amount=Sum('negative_amount'))
                    .filter(amount__gt=0)
                )
                self.queryset = Order.objects.filter(
                    pk__in=subquery.values_list('position', flat=True)
                )
            if (
                "date_from" in self.request.GET and
                "date_to" in self.request.GET
            ):
                filters.extend([
                    Q(order_date__gte=self.request.GET["date_from"]),
                    Q(order_date__lte=self.request.GET["date_to"])
                ])
            if "win" in self.request.GET:
                pass
                # filters.append()

        return self.queryset.filter(*filters)

    def get_serializer_class(self):
        if self.action in ["upload_excel_file"]:
            self.serializer_class = None
        if self.action in ["create", "update"]:
            self.serializer_class = OrderCreateSerializer
        if self.action in ["position"]:
            self.serializer_class = OrderPositionsSerializer
        return self.serializer_class

    @action(detail=False, methods=['post'])
    def upload_excel_file(self, request):
        fr = FileReader(request.FILES['files'], self.request)
        fr.return_as_dict()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def position(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
