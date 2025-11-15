from django.db import models
from usuarios.validadores import rfc_validador, curp_validador
from django.contrib.auth.models import User

class DatosPersonales(models.Model):
    rfc = models.CharField("R.F.C.", max_length=13, validators=[rfc_validador])
    curp = models.CharField("C.U.R.P.", max_length=18, validators=[curp_validador])
    direccion = models.CharField("Dirección", max_length=150)
    telefono = models.CharField("Teléfono", max_length=10)
    foto = models.ImageField(upload_to='perfil')
    user = models.OneToOneField(User, verbose_name="Usuario", related_name='datos', on_delete=models.DO_NOTHING)
    estado = models.ForeignKey("usuarios.Estado", verbose_name="Estado", on_delete=models.DO_NOTHING)
    municipio = models.ForeignKey("usuarios.Municipio", verbose_name="Municipio", on_delete=models.DO_NOTHING)
    
class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey("usuarios.Estado", verbose_name="Estado", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre    
    

