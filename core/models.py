from django.db import models
from django.contrib.auth.models import User


class productos(models.Model):
    serie =models.IntegerField(primary_key=True, verbose_name='Serie Producto')
    marca =models.CharField(max_length=50,verbose_name='Marca del Producto')
    codigo =models.CharField(max_length=50,verbose_name='Codigo del Producto')
    nombre =models.CharField(max_length=50,verbose_name='Nombre del Producto')
    fecha = models.DateTimeField(verbose_name='Fecha del Producto')
    valor = models.IntegerField(verbose_name='Precio del Producto')

    def __str__(self):
        return self.nombre

class ventas(models.Model):
    idVenta =models.IntegerField(primary_key=True, verbose_name='Id Venta')
    productosVendidos =models.ForeignKey(productos, on_delete=models.CASCADE)
    totalVenta = models.IntegerField(verbose_name='Precio del Producto')

    def __str__(self):
        return str(self.idVenta)   
    
    def save(self, *args, **kwargs):
        self.totalVenta = self.productosVendidos.valor
        super().save(*args, **kwargs)