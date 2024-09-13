from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'province', views.ProvinceView, basename='province')
router.register(r'city', views.CityView, basename='city')
router.register(r'address', views.AddressView, basename='address')


urlpatterns = router.urls
