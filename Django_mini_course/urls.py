from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from orders.views import *
from products.views import *
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# router = SimpleRouter()
# router.register('api/orders', OrderView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', orders_page),
    path("api/", include('hotel.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]

if (settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#urlpatterns += router.urls
