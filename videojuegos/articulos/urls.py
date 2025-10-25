from django.urls import path
from articulos import views, views_categoria

urlpatterns = [
    path('', views_categoria.BienvenidaView.as_view(), name='bienvenida'),
    
    path('articulos/', views.lista_articulos, name='articulos_lista'),
    path('articulos/nuevo', views.nuevo_articulo, name='nuevo_articulo'),
    path('articulos/eliminar/<int:id>', views.eliminar_articulos, name='eliminar_articulos'),
    path('articulos/editar/<int:id>', views.editar_articulos, name='editar_articulos'),

    # Clase basada en funcion   # Tarea
    # path('categorias/', views.lista_categorias, name='categorias_lista'),
    # path('categorias/nuevo', views.nueva_categoria, name='nueva_categoria'),
    # path('categorias/eliminar/<int:id>', views.eliminar_categoria, name='eliminar_categoria'),
    # path('categorias/editar/<int:id>', views.editar_categoria, name='editar_categoria'),

    # Clase basada en clase
    path('categorias/', views_categoria.ListaCategorias.as_view(), name='categorias_lista'),
    path('categorias/nuevo', views_categoria.NuevaCategoriaView.as_view(), name='nueva_categoria'),
    path('categorias/editar/<int:pk>', views_categoria.EditarCategoriaView.as_view(), name='editar_categoria'),
    path('categorias/eliminar/<int:pk>', views_categoria.EliminarCategoriaView.as_view(), name='eliminar_categoria'),

]
