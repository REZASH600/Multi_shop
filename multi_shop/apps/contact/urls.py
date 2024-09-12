from django.urls import path
from . import views

app_name = "contact_app"
urlpatterns = [
    path("", views.ContactView.as_view(), name="contact"),
    
    ]
