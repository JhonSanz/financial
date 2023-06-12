from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.user.urls')),
    path('api/', include('apis.order.urls')),
    path('api/', include('apis.currency.urls')),
]