from django.urls import path
from .views import register, verify_email, user_login

urlpatterns = [
    path('', register, name='register'),
    path('verify-email/<int:user_id>/<str:otp>/', verify_email, name='verify_email'),
    path('login/', user_login, name='login'),
]
