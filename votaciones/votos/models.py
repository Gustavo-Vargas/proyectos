from django.db import models
import os

def partido_foto_path(instance, filename):
    return os.path.join('partido', filename)

def candidato_foto_path(instance, filename):
    return os.path.join('candidato', filename)

class Partido(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField('Descripcion', null=True, blank=True)
    foto = models.ImageField(upload_to=partido_foto_path, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Candidato(models.Model):
    nombre = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=50)
    ap_materno = models.CharField(max_length=50)
    foto = models.ImageField(upload_to=candidato_foto_path, null=True, blank=True)
    partido = models.ForeignKey("votos.Partido", verbose_name="Partido", on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.nombre} {self.ap_paterno} {self.ap_materno}"

class Votacion(models.Model):
    candidato = models.ForeignKey("votos.Candidato", verbose_name="Candidato", on_delete=models.DO_NOTHING)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Voto para {self.candidato} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
    