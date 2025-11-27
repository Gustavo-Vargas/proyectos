from django.contrib import admin
from votos.models import Partido, Candidato, Votacion

admin.site.register(Partido)
admin.site.register(Candidato)
admin.site.register(Votacion)
