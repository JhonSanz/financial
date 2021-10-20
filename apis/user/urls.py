
from django.urls import path
from rest_framework import routers
from apis.user.views.authentication import CustomTokenObtainPairView, Logout
from apis.user.views.user import UserApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

router = routers.SimpleRouter()
router.register(r'user', UserApi,
                basename='user')

urlpatterns = [
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('logout', Logout.as_view(), name='logout'),
]
urlpatterns += router.urls
