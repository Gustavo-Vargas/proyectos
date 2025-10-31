from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from articulos.models import Articulos, Categoria, ArticuloFoto
from articulos.forms import FormArticulo, FormCategoria, ArticuloFotoFormSet
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods

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
        