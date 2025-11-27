from django.shortcuts import render, redirect
from votos.models import Partido, Candidato
from django.views.generic import TemplateView
from votos.forms import PartidoForm, CandidatoForm

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
        form = PartidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('partidos_lista')
    else:    
        form = PartidoForm()
    return render(request, 'partido_form.html', {'form':form})
    
def editar_partido(request, id):
    partido = Partido.objects.get(id=id)
    foto_anterior_path = None
    
    if request.method == 'POST':
        if partido.foto:
            foto_anterior_path = partido.foto.path
        
        form = PartidoForm(request.POST, request.FILES, instance=partido)
        if form.is_valid():
            if foto_anterior_path and 'foto' in request.FILES:
                import os
                if os.path.exists(foto_anterior_path):
                    os.remove(foto_anterior_path)
            form.save()
            return redirect('partidos_lista')
    else: 
        form = PartidoForm(instance=partido)
    return render(request, 'partido_form.html', {'form':form})

# Candidatos
def lista_candidatos(request):
    candidatos = Candidato.objects.all()
    
    return render(request, 'candidatos.html', {'candidatos': candidatos})

def eliminar_candidato(request, id):
    Candidato.objects.get(id=id).delete()
    return redirect('candidatos_lista')
    
def nuevo_candidato(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidatos_lista')
    else:    
        form = CandidatoForm()
    return render(request, 'candidato_form.html', {'form':form})
    
def editar_candidato(request, id):
    candidato = Candidato.objects.get(id=id)
    foto_anterior_path = None
    
    if request.method == 'POST':
        if candidato.foto:
            foto_anterior_path = candidato.foto.path
        
        form = CandidatoForm(request.POST, request.FILES, instance=candidato)
        if form.is_valid():
            if foto_anterior_path and 'foto' in request.FILES:
                import os
                if os.path.exists(foto_anterior_path):
                    os.remove(foto_anterior_path)
            form.save()
            return redirect('candidatos_lista')
    else: 
        form = CandidatoForm(instance=candidato)
    return render(request, 'candidato_form.html', {'form':form})
