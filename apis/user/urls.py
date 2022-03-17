
from django.urls import path
from rest_framework import routers
from apis.user.views.authentication import CustomTokenObtainPairView, Logout
from apis.user.views.user import UserApi
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register(r'user', UserApi,
                basename='user')

urlpatterns = [
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
urlpatterns += router.urls
