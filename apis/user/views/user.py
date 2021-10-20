
from rest_framework import viewsets
from apis.user.serializers.user import UserSerializer, UserCreateSerializer
from apps.user.models import User
from rest_framework.permissions import IsAuthenticated
from apis.utils.paginator import CustomPagination


class UserApi(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        filters = []
        if self.action in ["list"]:
            self.queryset = User.objects.all()
        return self.queryset.filter(*filters)

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            self.serializer_class = UserCreateSerializer
        return self.serializer_class
