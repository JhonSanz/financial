
from django.urls import path
from rest_framework import routers
from apis.order.views.order import OrderApi

router = routers.SimpleRouter()
router.register(r'order', OrderApi,
                basename='order')

urlpatterns = []
urlpatterns += router.urls
