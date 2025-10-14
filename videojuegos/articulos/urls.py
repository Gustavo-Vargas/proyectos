from django.urls import path
from articulos import views

urlpatterns = [
    path('', views.lista_articulos, name='articulos_lista'),
    path('nuevo', views.nuevo_articulo, name='nuevo_articulo'),
    path('eliminar/<int:id>', views.eliminar_articulos, name='eliminar_articulos'),
    path('editar/<int:id>', views.editar_articulos, name='editar_articulos'),

    path('categorias/', views.lista_categorias, name='categorias_lista'),
    path('categorias/nuevo', views.nueva_categoria, name='nueva_categoria'),
    path('categorias/eliminar/<int:id>', views.eliminar_categoria, name='eliminar_categoria'),
    path('categorias/editar/<int:id>', views.editar_categoria, name='editar_categoria'),
]
