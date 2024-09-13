from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('products/',include('apps.product.urls')),
    path('accounts/', include('apps.account.urls')),
    path('carts/', include('apps.cart.urls')),
    path('contacts/', include('apps.contact.urls')),

    path('accounts/api/', include('apps.account.api.urls')),
    path('products/api/', include('apps.product.api.urls')),
    path('orders/api/', include('apps.order.api.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  

 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
