from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser
from apis.order.serializers.order import OrderSerializer, OrderCreateSerializer
from apps.order.models import Order
from apis.utils.paginator import CustomPagination
from apis.order.utils.excel_file import FileReader


class OrderApi(viewsets.ModelViewSet):
    queryset = Order.objects
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    parser_class = (MultiPartParser, JSONParser)

    def get_queryset(self):
        filters = []
        if self.action in ["list"]:
            self.queryset = Order.objects.filter(owner=self.request.user)
        return self.queryset.filter(*filters)

    def get_serializer_class(self):
        if self.action in ["upload_excel_file"]:
            self.serializer_class = None
        if self.action in ["create", "update"]:
            self.serializer_class = OrderCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=['post'])
    def upload_excel_file(self, request):
        fr = FileReader(request.FILES['files'], self.request)
        data = fr.return_as_dict()
        return Response({}, status=status.HTTP_200_OK)
