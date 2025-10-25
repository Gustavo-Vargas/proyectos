from sre_parse import SUCCESS
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from articulos.forms import FormCategoria
from articulos.models import Categoria, Articulos
from django.contrib import messages
from django.http import HttpResponseRedirect



class ListaCategorias(ListView):
    model = Categoria
    paginate_by = 5
    template_name = 'articulos/categoria_list.html'
    context_object_name = 'object_list'


class NuevaCategoriaView(CreateView):
    model = Categoria
    form_class = FormCategoria
    success_url = reverse_lazy('categorias_lista')
    extra_context = {'accion': 'Nueva'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada con éxito.')
        return super().form_valid(form)
    

class EditarCategoriaView(UpdateView):
    model = Categoria
    fields = '__all__'
    success_url = reverse_lazy('categorias_lista')
    extra_context = {'accion': 'Modificar'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría modificada con éxito.')
        return super().form_valid(form)

class EliminarCategoriaView(DeleteView):
    model = Categoria
    success_url = reverse_lazy('categorias_lista')
    
    def form_valid(self, form):
        self.object = self.get_object()
        if Articulos.objects.filter(categoria=self.object).exists():
            messages.error(self.request, 'No se puede eliminar la categoría; tiene artículos creados.')
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            self.object.delete()
            messages.success(self.request, 'Se eliminó con éxito.')
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)

class BienvenidaView(TemplateView):
    template_name = 'bienvenida.html'


