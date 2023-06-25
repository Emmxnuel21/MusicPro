from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import productos, ventas

admin.site.register(Permission)
admin.site.register(productos)
admin.site.register(ventas)

