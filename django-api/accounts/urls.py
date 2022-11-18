from django.urls import path
from . import views

urlpatterns = [
    path('otp/', views.OTPView.as_view(), name='otp-view'),
]