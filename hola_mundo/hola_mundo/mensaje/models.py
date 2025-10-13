from django.db import models

# Create your models here.

PRESENTACION = [
    ('1', 'Caja'),
    ('2', 'Pieza'),
    ('3', 'Paquete'),
]

COLOR = [
    ('r', 'Rojo'),
    ('a', 'Azul'),
    ('v', 'Verde'),
]
class Articulos(models.Model):
    nombre = models.CharField(max_length=50)
    description = models.TextField('Descripción', null=True, blank=True)
    stock = models.IntegerField()
    presentacion = models.CharField('Presentacizión', max_length=1, choices=PRESENTACION)
    color = models.CharField(max_length=1, choices=COLOR, default='a')
    
    def __str__(self):
        return self.nombre

