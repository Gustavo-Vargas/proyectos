from django.urls import path
from votos import views

urlpatterns = [
    path('', views.BienvenidaView.as_view(), name='bienvenida'),
    path('partidos', views.lista_partidos, name="partidos_lista"),
    path('partidos/nuevo', views.nuevo_partido, name="nuevo_partido"),
    path('partido/eliminar/<int:id>', views.eliminar_partido, name="eliminar_partido"),
    path('partido/editar/<int:id>', views.editar_partido, name="editar_partido"),
]


