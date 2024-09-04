from django.urls import path
from . import views


app_name = "product_app"

urlpatterns = [
    path("detail/<slug:slug>/", views.ProductDetailView.as_view(), name="detail"),
    path("list/", views.ProductListView.as_view(), name="list"),
    path("like/<int:product_id>/", views.LikeView.as_view(), name="like"),
]
