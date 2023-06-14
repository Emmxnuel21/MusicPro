from django.urls import path
from .views import crearCuenta, index

urlpatterns =[
    path('', index,name="index"),
    path('register/', crearCuenta, name="register"),
]