from django.urls import path
from .views import accesorios, bodega, contabilidad, crearCuenta, form_add_productos, form_add_ventas, form_del_productos, form_del_ventas, form_mod_productos, form_mod_ventas, guitarras,index, vendedor, webpay_plus_commit

urlpatterns =[

    path('', index,name="index"),
    path('register/', crearCuenta, name="register"),
    path('ventas/', vendedor, name="ventas"),
    path('bodega/', bodega, name="bodega"),
    path('contabilidad/', contabilidad, name="contabilidad"),
    path('commit/', webpay_plus_commit, name="commit"),
    
    #VENTAS DE PRODUCTOS
    path('guitarras/', guitarras, name="guitarras"),
    path('accesorios/', accesorios, name="accesorios"),
    # PRODUCTOS

    path('form-add-productos', form_add_productos, name="form_add_productos"),
    path('form-mod-productos/<id>', form_mod_productos, name="form_mod_productos"),
    path('form-del-productos/<id>', form_del_productos, name="form_del_productos"),

    #VENTAS

    path('form-add-ventas', form_add_ventas, name="form_add_ventas"),
    path('form-mod-ventas/<id>', form_mod_ventas, name="form_mod_ventas"),
    path('form-del-ventas/<id>', form_del_ventas, name="form_del_ventas"),
]