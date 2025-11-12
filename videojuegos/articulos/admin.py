from django.contrib import admin
from articulos.models import Articulos, Categoria, Venta, DetalleVenta

admin.site.register(Articulos)
admin.site.register(Categoria)
admin.site.register(Venta)
admin.site.register(DetalleVenta)