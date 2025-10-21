from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from articulos.models import Articulos, Categoria


class ListaCategorias(ListView):
    model = Categoria
    # queryset = Categoria.objects.order_by('nombre')


class NuevaCategoriaView (CreateView):
    modelo = Categoria
    fields = '__all__'  
    success_url = reverse_lazy('categorias_lista')

class EditarCategoriaView(UpdateView):
    model = Categoria
    fields = '__all__'
    success_url = reverse_lazy('categorias_lista')

class BienvenidaView(TemplateView):
    template_name = 'bienvenida.html'


