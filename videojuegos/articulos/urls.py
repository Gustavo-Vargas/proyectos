from django.urls import path
from articulos import views, views_categoria

urlpatterns = [
    path('', views_categoria.BienvenidaView.as_view(), name='bienvenida'),
    
    path('articulos/', views.lista_articulos, name='articulos_lista'),
    path('articulos/nuevo', views.nuevo_articulo, name='nuevo_articulo'),
    path('articulos/eliminar/<int:id>', views.eliminar_articulos, name='eliminar_articulos'),
    path('articulos/editar/<int:id>', views.editar_articulos, name='editar_articulos'),
    path('articulos/<int:id>/fotos', views.gestionar_fotos_articulo, name='gestionar_fotos_articulo'),
    path('articulos/<int:id>/fotos/<int:foto_id>/eliminar', views.eliminar_foto_articulo, name='eliminar_foto_articulo'),

    path('articulos/tienda', views.ArticuloTiendaView.as_view(), name='articulos_tienda'),
    path('articulos/carrito/<int:pk>/agregar/', views.agregar_al_carrito, name='carrito_agregar'),
    path('articulos/carrito/<int:pk>/actualizar/', views.actualizar_cantidad_carrito, name='carrito_actualizar'),
    path('articulos/carrito/<int:pk>/eliminar/', views.eliminar_del_carrito, name='carrito_eliminar'),
    path('articulos/carrito', views.carrito_resumen, name='carrito_resumen'),
    path('articulos/carrito/finalizar', views.finalizar_compra, name='carrito_finalizar'),
    
    path('ventas/', views.ListaVentasView.as_view(), name='ventas_lista'),
    
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
