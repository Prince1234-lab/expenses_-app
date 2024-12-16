from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.userperferences, name='userperferences')
]
