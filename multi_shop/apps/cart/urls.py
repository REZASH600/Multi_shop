from django.urls import path
from . import views

app_name = "cart_app"
urlpatterns = [
    path("list/", views.CartView.as_view(), name="list_cart"),
    path(
        "product/remove/<str:unique_name>/",
        views.RemoveProductView.as_view(),
        name="remove_product",
    ),
    path(
        "change/quantity/<str:unique_name>/<str:value>/",
        views.AddSubtractQuantityView.as_view(),
        name="add_subtract_quantity",
    ),
]
