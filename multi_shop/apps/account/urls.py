from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('check/otp/', views.CheckOtpView.as_view(), name='check_otp'),
    path('resend/code/', views.ResendCodeView.as_view(), name='resend_code'),
    path('forgot/password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset/password/<token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
