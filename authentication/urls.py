from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView,LoginView,LogoutView
from django.views.decorators.csrf import csrf_exempt


app_name = 'authentication'


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
    path('validation-username', csrf_exempt(UsernameValidationView.as_view()), name='validation-username'),
    path('validation-email', csrf_exempt(EmailValidationView.as_view()), name='validation-email'),
    path('activate/<str:uid64>/<str:token>', VerificationView.as_view(), name= 'activate' ),
]
