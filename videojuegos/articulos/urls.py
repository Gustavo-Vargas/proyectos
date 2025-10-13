from django.urls import path
from articulos import views

urlpatterns = [
    path('', views.lista_articulos, name='articulos_lista'),
    path('nuevo', views.nuevo_articulo, name='nuevo_articulo'),
    path('eliminar/<int:id>', views.eliminar_articulos, name='eliminar_articulos'),
    path('editar/<int:id>', views.editar_articulos, name='editar_articulos'),
]
