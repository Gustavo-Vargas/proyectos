from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from articulos.forms import ArticuloFotoFormSet, FormArticulo, FormCategoria
from articulos.models import ArticuloFoto, Articulos, Categoria, Venta, DetalleVenta, ESTADOS_VENTA

# Articulos
@permission_required('add_articulos')
def lista_articulos(request):
    articulos_list = Articulos.objects.all()
       # articulos = Articulos.objects.order_by('-stock','nombre')
    # articulos = Articulos.objects.filter(genero='1')
    
    paginator = Paginator(articulos_list, 10)
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)

    return render(request, 'articulos.html', {'articulos': articulos})

def eliminar_articulos(request, id):
    Articulos.objects.get(id=id).delete()
    messages.error(request, 'Artículo eliminado con exito.')
    return redirect('articulos_lista')
    
def nuevo_articulo(request):
    if request.method == 'POST':
        form = FormArticulo(request.POST)
        # print(form)
        if form.is_valid():
           form.save()
           messages.success(request, 'Artículo creado con éxito.')
           return redirect('articulos_lista')
    else: 
        form = FormArticulo()
    return render(request, 'nuevo_articulo.html', {'form':form})
    
def editar_articulos(request, id):
    articulo = Articulos.objects.get(id=id)
    if request.method == 'POST':
        form = FormArticulo(request.POST, instance=articulo)
        if form.is_valid():
           form.save()
           messages.success(request, 'Artículo modificado con éxito.')
           return redirect('articulos_lista')
            
    else: 
        form = FormArticulo(instance=articulo)
    return render(request, 'editar_articulo.html', {'form':form})
 

@require_http_methods(["GET", "POST"])
def gestionar_fotos_articulo(request, id):
    articulo = Articulos.objects.get(id=id)
    if request.method == 'POST':
        formset = ArticuloFotoFormSet(request.POST, request.FILES, instance=articulo, queryset=ArticuloFoto.objects.none())
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Fotos actualizadas con éxito.')
            return redirect('gestionar_fotos_articulo', id=articulo.id)
    else:
        formset = ArticuloFotoFormSet(instance=articulo, queryset=ArticuloFoto.objects.none())
    return render(request, 'articulos/gestionar_fotos.html', {'articulo': articulo, 'formset': formset})

@require_http_methods(["POST"])
def eliminar_foto_articulo(request, id, foto_id):
    articulo = Articulos.objects.get(id=id)
    foto = articulo.fotos.get(id=foto_id)
    foto.delete()
    messages.success(request, 'Foto eliminada con éxito.')
    return redirect('gestionar_fotos_articulo', id=articulo.id)


# Tienda
class ArticuloTiendaView(ListView):
    model = Articulos
    template_name = 'articulos_tienda.html'
    context_object_name = 'articulos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        disponibles = {}
        for pk, data in cart.items():
            try:
                disponibles[int(pk)] = int(data.get('cantidad', 0))
            except (TypeError, ValueError):
                disponibles[int(pk)] = 0
        for articulo in context['articulos']:
            en_carrito = disponibles.get(articulo.id, 0)
            stock_disponible = max(articulo.stock - en_carrito, 0)
            articulo.stock_disponible = stock_disponible
        return context

    def get_queryset(self):
        return Articulos.objects.filter(stock__gt=0).prefetch_related('fotos', 'categoria').order_by('nombre')

# Carrito
@require_http_methods(["POST"])
def agregar_al_carrito(request, pk):
    cart = _cart(request)
    articulo = Articulos.objects.filter(pk=pk, stock__gt=0).first()
    if not articulo:
        messages.error(request, 'Artículo sin stock.')
        return redirect('articulos_tienda')
    key = str(articulo.pk)
    item = cart.get(key, {'cantidad': 0, 'nombre': articulo.nombre})
    item['nombre'] = articulo.nombre
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        cantidad = 1
    if cantidad < 1:
        messages.warning(request, 'Ingresa una cantidad válida.')
        return redirect('articulos_tienda')
    if cantidad > articulo.stock:
        messages.warning(request, f'Solo hay {articulo.stock} unidades disponibles.')
        return redirect('articulos_tienda')
    existente = item.get('cantidad', 0)
    disponible = articulo.stock - existente
    if disponible <= 0:
        messages.warning(request, 'Ya tienes en el carrito todas las unidades disponibles.')
        return redirect('articulos_tienda')
    if cantidad > disponible:
        messages.warning(request, f'Solo quedan {disponible} unidades disponibles.')
        return redirect('articulos_tienda')
    item['cantidad'] = existente + cantidad
    cart[key] = item
    _save(request)
    messages.success(request, f'Se agregaron {cantidad} unidades al carrito.')
    return redirect('articulos_tienda')


@require_http_methods(["POST"])
def actualizar_cantidad_carrito(request, pk):
    cart = _cart(request)
    key = str(pk)
    item = cart.get(key)
    if not item:
        messages.warning(request, 'El artículo no está en el carrito.')
        return redirect('carrito_resumen')
    articulo = Articulos.objects.filter(pk=pk).first()
    if not articulo:
        cart.pop(key, None)
        _save(request)
        messages.error(request, 'El artículo ya no está disponible.')
        return redirect('carrito_resumen')
    accion = request.POST.get('accion')
    if accion == 'incrementar':
        if item['cantidad'] >= articulo.stock:
            messages.warning(request, f'Solo hay {articulo.stock} unidades disponibles.')
        else:
            item['cantidad'] += 1
            cart[key] = item
            _save(request)
            messages.success(request, 'Cantidad incrementada.')
    elif accion == 'decrementar':
        if item['cantidad'] <= 1:
            messages.warning(request, 'La cantidad mínima es 1.')
        else:
            item['cantidad'] -= 1
            cart[key] = item
            _save(request)
            messages.success(request, 'Cantidad reducida.')
    return redirect('carrito_resumen')


@require_http_methods(["POST"])
def eliminar_del_carrito(request, pk):
    cart = _cart(request)
    key = str(pk)
    if cart.pop(key, None) is not None:
        _save(request)
        messages.success(request, 'Artículo eliminado del carrito.')
    else:
        messages.warning(request, 'El artículo no está en el carrito.')
    return redirect('carrito_resumen')


def _cart(request):
    return request.session.setdefault('cart', {})


def _save(request):
    request.session.modified = True


def carrito_resumen(request):
    cart = _cart(request)
    if not cart:
        return render(request, 'carrito_resumen.html', {'items': [], 'total_items': 0, 'total_amount': Decimal('0.00')})
    ids = [int(pk) for pk in cart.keys()]
    articulos = Articulos.objects.filter(pk__in=ids).prefetch_related('fotos', 'categoria')
    items = []
    total_amount = Decimal('0.00')
    for articulo in articulos:
        data = cart.get(str(articulo.pk), {})
        cantidad = data.get('cantidad', 0)
        if cantidad > 0:
            subtotal = (articulo.precio or Decimal('0.00')) * cantidad
            total_amount += subtotal
            items.append({'articulo': articulo, 'cantidad': cantidad, 'subtotal': subtotal})
    items.sort(key=lambda item: item['articulo'].nombre.lower())
    total_items = sum(item['cantidad'] for item in items)
    return render(request, 'carrito_resumen.html', {'items': items, 'total_items': total_items, 'total_amount': total_amount})

# Compra/venta
def crear_venta(request):
    # Verifica que el usairo este autenticado
    if not request.user.is_authenticated:
        messages.warning(request, 'Necesita iniciar sesion para hacer la compra')
    # obtener el carrito via _cart(request)
    cart = _cart(request)
    if not cart:
        messages.warning(request, 'No tiene articulso en el carrito')
    
    # Crear la venta base: 
    venta = Venta.objects.create(cliente=request.user, total=Decimal('0.00'))
    total = Decimal('0.00')
    
    # Recorrer los articulos al carrito
    for pk, item in cart.items():
        cantidad = int(item.get('cantidad', 0))
        if cantidad <= 0:
            continue
        articulo = Articulos.objects.select_for_update().filter(pk=pk).first()
        if not articulo:
            messages.error(request, 'Articulo no disponible')
        if articulo.stock < cantidad:
            messages.error(request, 'Articulo sin suficiente stock')
        precio_unitario = articulo.precio
        subtotal = precio_unitario * cantidad
        DetalleVenta.objects.create(
            venta=venta,
            articulo=articulo,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )
        articulo.stock -= cantidad
        articulo.save(update_fields=['stock'])
        total += subtotal
    venta.total = total
    venta.save(update_fields=['total'])
    request.session['cart'] = {}
    _save(request)
    return venta
                
@login_required
@require_POST
def finalizar_compra(request):
    cart = _cart(request)
    if not cart:
        messages.warning(request, 'Tu carrito esta vacio')
        return redirect('carrito_resumen')
    try:
        with transaction.atomic():
            venta = crear_venta(request)
    except ValidationError as error:
        messages.error(request, error.message)
        return redirect('carrito_resumen')
    
    messages.success(request, 'Compra registrada')
    return redirect('carrito_resumen')

    
# @permission_required('view_venta')
class ListaVentasView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas.html'
    context_object_name = 'ventas'
    # paginate_by = 10
    ordering = ('-creada_en',)

    def get_queryset(self):
        queryset = super().get_queryset().select_related('cliente').prefetch_related('detalles__articulo')
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ESTADOS_VENTA
        context['estado_actual'] = self.request.GET.get('estado', '')
        return context
    

# Categorias
def lista_categorias(request):
    categorias = Categoria.objects.all()

    return render(request, 'categorias.html',
    {'categorias': categorias})

def eliminar_categoria(request, id):
    # context = {}
    # categoria = Categoria.objects.get(categoria=categoria)
    # articulos = Articulos.objects.filter(categoria=categorias)
    # if articulos: 
    # else: 
    # try: 
        Categoria.objects.get(id=id).delete()
        messages.error(request, 'Categoría eliminada con éxito.')
    # except:
    #     context['mensaje'] = 'No se puede eliminar la categoria porque tiene articulos'
        return redirect('categorias_lista')

def nueva_categoria(request):
    if request.method == 'POST':
        form = FormCategoria(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('categorias_lista')

    else:
        form = FormCategoria()
    return render(request, 'nueva_categoria.html',
    {'form': form})

def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == 'POST':
        form = FormCategoria(request.POST,
        instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría modificada con éxito.')
            return redirect('categorias_lista')
    else: 
        form = FormCategoria(instance=categoria)
    return render(request, 'editar_categoria.html', {'form':form}) 


class ListaArticulosView(ListView):
    model = Articulos
    template_name = 'articulos.html'
    context_object_name = 'articulos'


class NuevoArticuloView(CreateView):
    model = Articulos
    form_class = FormArticulo
    template_name = 'nuevo_articulo.html'
    success_url = reverse_lazy('articulos_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Artículo creado con éxito.')
        return super().form_valid(form)


class EditarArticuloView(UpdateView):
    model = Articulos
    form_class = FormArticulo
    template_name = 'editar_articulo.html'
    success_url = reverse_lazy('articulos_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Artículo modificado con éxito.')
        return super().form_valid(form)


class EliminarArticuloView(DeleteView):
    model = Articulos
    success_url = reverse_lazy('articulos_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Artículo eliminado con éxito.')
        return super().delete(request, *args, **kwargs)
        