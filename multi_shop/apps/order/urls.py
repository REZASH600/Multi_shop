from django.urls import path
from . import views

app_name = "order_app"
urlpatterns = [
    path('checkout/',views.CheckoutView.as_view(),name="checkout"),
    path('get/cities/',views.LoadCitesView.as_view(),name="get_cities")
]
