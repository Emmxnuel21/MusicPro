from django.urls import path
from .views import bodega, contabilidad, crearCuenta, form_del_productos, form_mod_productos, index, ventas

urlpatterns =[
    path('', index,name="index"),
    path('register/', crearCuenta, name="register"),
    path('ventas/', ventas, name="ventas"),
    path('bodega/', bodega, name="bodega"),
    path('contabilidad/', contabilidad, name="contabilidad"),
    path('form-mod-pacientes/<id>', form_mod_productos, name="form_mod_productos"),
    path('form-del-pacientes/<id>', form_del_productos, name="form_del_productos"),
]