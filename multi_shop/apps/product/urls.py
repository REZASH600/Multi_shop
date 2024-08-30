from django.urls import path
from . import views


app_name = "product_app"

urlpatterns = [
    path("detail/<slug:slug>/", views.ProductDetailView.as_view(), name="detail")
]
