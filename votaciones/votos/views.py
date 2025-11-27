from django.shortcuts import render, redirect
from votos.models import Partido
from django.views.generic import TemplateView
from votos.forms import PartidoForm

class BienvenidaView(TemplateView):
    template_name = 'bienvenida.html'

def lista_partidos(request):
    partidos = Partido.objects.all()
    
    return render(request, 'partidos.html', {'partidos': partidos})

def eliminar_partido(request, id):
    Partido.objects.get(id=id).delete()
    return redirect('partidos_lista')
    
def nuevo_partido(request):
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partidos_lista')
    else:    
        form = PartidoForm()
    return render(request, 'nuevo_partido.html', {'form':form})
    
def editar_partido(request, id):
    partido = Partido.objects.get(id=id)
    if request.method == 'POST':
        form = PartidoForm(request.POST, instance=partido)
        if form.is_valid():
           form.save()
        #    messages.success(request, 'Partido modificado con éxito.')
           return redirect('partidos_lista')
            
    else: 
        form = PartidoForm(instance=partido)
    return render(request, 'editar_partido.html', {'form':form})