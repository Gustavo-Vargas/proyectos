from django.urls import path
from votos import views

urlpatterns = [
    path('', views.BienvenidaView.as_view(), name='bienvenida'),
    path('partidos', views.lista_partidos, name="partidos_lista"),
    path('partidos/nuevo', views.nuevo_partido, name="nuevo_partido"),
    path('partido/eliminar/<int:id>', views.eliminar_partido, name="eliminar_partido"),
    path('partido/editar/<int:id>', views.editar_partido, name="editar_partido"),
    
    path('partidos-publicos', views.partidos_publicos, name="partidos_publicos"),
    path('partido/<int:partido_id>/candidatos', views.candidatos_por_partido, name="candidatos_por_partido"),
    path('candidatos-publicos', views.candidatos_publicos, name="candidatos_publicos"),
    
    path('candidatos', views.lista_candidatos, name="candidatos_lista"),
    path('candidatos/nuevo', views.nuevo_candidato, name="nuevo_candidato"),
    path('candidato/eliminar/<int:id>', views.eliminar_candidato, name="eliminar_candidato"),
    path('candidato/editar/<int:id>', views.editar_candidato, name="editar_candidato"),
    
]


