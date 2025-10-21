from django.shortcuts import render, redirect
from articulos.models import Articulos, Categoria
from articulos.forms import FormArticulo, FormCategoria

def lista_articulos(request):
    # articulos = Articulos.objects.all()
    # articulos = Articulos.objects.order_by('-stock','nombre')
    articulos = Articulos.objects.filter(genero='1')
    print(articulos.query)
    len(articulos)
    Articulos.objects.count()

    return render(request, 'articulos.html', {'articulos': articulos})

def eliminar_articulos(request, id):
    Articulos.objects.get(id=id).delete()
    return redirect('articulos_lista')
    
def nuevo_articulo(request):
    if request.method == 'POST':
        form = FormArticulo(request.POST)
        # print(form)
        if form.is_valid():
           form.save()
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
           return redirect('articulos_lista')
            
    else: 
        form = FormArticulo(instance=articulo)
    return render(request, 'editar_articulo.html', {'form':form})
    

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
    # except:
    #     context['mensaje'] = 'No se puede eliminar la categoria porque tiene articulos'
        return redirect('categorias_lista')

def nueva_categoria(request):
    if request.method == 'POST':
        form = FormCategoria(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('categorias_lista')
    else: 
        form = FormCategoria(instance=categoria)
    return render(request, 'editar_categoria.html', {'form':form}) 
        