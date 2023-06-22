from django.db import models
from django.contrib.auth.models import User

class productos(models.Model):
    idProducto =models.IntegerField(primary_key=True, verbose_name='Id Producto')
    nombreProducto =models.CharField(max_length=50,verbose_name='Nombre del Producto')
    precioProducto =models.IntegerField(verbose_name='Precio del Producto')
    def __str__(self):
        return self.nombreProducto
    
class ventas(models.Model):
    idVenta =models.IntegerField(primary_key=True, verbose_name='Id Venta')
    productosVendidos =models.CharField(max_length=50,verbose_name='Nombre de los Productos')
    totalVenta =models.IntegerField(verbose_name='Precio final de compra')
    def __str__(self):
        return self.producto1    