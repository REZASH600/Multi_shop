from django.urls import path
from . import views

app_name = "order_app"
urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("get/cities/", views.LoadCitesView.as_view(), name="get_cities"),
    path("creation/", views.OrderCreationView.as_view(), name="order_creation"),
    path("detail/<int:id>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("change/address/", views.ChangeAddressView.as_view(), name="change_address"),
    path('remove/products/<int:order_id>/<int:order_item_id>/',views.RemoveProductOrderView.as_view(),name="remove_product")
]
