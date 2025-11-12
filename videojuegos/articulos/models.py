from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

GENERO = [
    ('1', 'Acción'),
    ('2', 'Aventura'),
    ('3', 'Carrera'),
]

ESTADOS_VENTA = [
    ('pendiente', 'Pendiente'),
    ('pagada', 'Pagada'),
    ('cancelada', 'Cancelada'),
]

class Articulos(models.Model):
    nombre = models.CharField(max_length=50)
    description = models.TextField('Descripción', null=True, blank=True)
    stock = models.IntegerField(default=0, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    genero = models.CharField('Género', max_length=1, choices=GENERO)
    categoria = models.ForeignKey("articulos.Categoria", verbose_name="Categoria", on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nombre
    
def articulo_image_upload_path(instance, filename):
    return f"articulo/{instance.articulo_id}/{filename}"

class ArticuloFoto(models.Model):
    articulo = models.ForeignKey(Articulos, related_name='fotos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=articulo_image_upload_path)
    creado_en = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            anterior = ArticuloFoto.objects.get(pk=self.pk)
            if anterior.imagen and self.imagen and anterior.imagen.name != self.imagen.name:
                anterior.imagen.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        nombre = self.imagen.name if self.imagen else None
        super().delete(*args, **kwargs)
        if nombre:
            self._meta.get_field('imagen').storage.delete(nombre)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField('Descripcion', max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nombre


@receiver(post_delete, sender=ArticuloFoto)
def articulo_foto_post_delete(sender, instance, **kwargs):
    if instance.imagen:
        storage = instance._meta.get_field('imagen').storage
        storage.delete(instance.imagen.name)

class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ventas')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS_VENTA, default='pendiente')
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Venta #{self.id}'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    articulo = models.ForeignKey(Articulos, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)
