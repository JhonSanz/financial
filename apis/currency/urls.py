
from rest_framework import routers
from apis.currency.views.currency import CurrencyApi

router = routers.SimpleRouter()
router.register(r'currency', CurrencyApi,
                basename='currency')

urlpatterns = []
urlpatterns += router.urls
