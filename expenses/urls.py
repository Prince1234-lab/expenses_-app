from django.urls import path
from . import views




urlpatterns = [
    path('expenses', views.index, name='expenses'),
    path('add_expense', views.add_expense, name="add_expense"),
]
