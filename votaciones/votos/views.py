from django.shortcuts import render, redirect, get_object_or_404
from votos.models import Partido, Candidato, Votacion
from django.views.generic import TemplateView
from votos.forms import PartidoForm, CandidatoForm
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

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

# Ventanas públicas
def partidos_publicos(request):
    partidos = Partido.objects.all()
    return render(request, 'partidos_publicos.html', {'partidos': partidos})

def candidatos_publicos(request):
    candidatos = Candidato.objects.select_related('partido').all()
    return render(request, 'candidatos_publicos.html', {'candidatos': candidatos})

def candidatos_por_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    candidatos = Candidato.objects.filter(partido=partido).select_related('partido')
    return render(request, 'candidatos_por_partido.html', {
        'partido': partido,
        'candidatos': candidatos
    })

def votar(request):
    candidatos = Candidato.objects.select_related('partido').all()
    return render(request, 'votar.html', {'candidatos': candidatos})

def procesar_voto(request, candidato_id):
    if request.method == 'POST':
        candidato = get_object_or_404(Candidato, id=candidato_id)
        Votacion.objects.create(candidato=candidato)
        messages.success(request, f'¡Voto registrado exitosamente para {candidato}!')
        return redirect('resultados')
    return redirect('votar')

def resultados(request):
    candidatos_con_votos = (
        Candidato.objects
        .select_related('partido')
        .annotate(total_votos=Count('votacion'))
        .filter(total_votos__gt=0)
        .order_by('-total_votos')
    )
    
    total_votos = Votacion.objects.count()
    
    return render(request, 'resultados.html', {
        'candidatos_con_votos': candidatos_con_votos,
        'total_votos': total_votos
    })

def dashboard(request):
    # Estadísticas generales
    total_votos = Votacion.objects.count()
    total_candidatos = Candidato.objects.count()
    total_partidos = Partido.objects.count()
    
    # Votos por partido
    votos_por_partido = (
        Partido.objects
        .annotate(total_votos=Count('candidato__votacion'))
        .order_by('-total_votos')
    )
    
    # Top 5 candidatos
    top_candidatos = (
        Candidato.objects
        .select_related('partido')
        .annotate(total_votos=Count('votacion'))
        .filter(total_votos__gt=0)
        .order_by('-total_votos')[:5]
    )
    
    # Votos recientes (últimas 24 horas)
    hace_24_horas = timezone.now() - timedelta(hours=24)
    votos_recientes = Votacion.objects.filter(fecha_hora__gte=hace_24_horas).count()
    
    # Votos por hora del día (últimas 24 horas)
    votos_por_hora = []
    for i in range(24):
        hora_inicio = timezone.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=23-i)
        hora_fin = hora_inicio + timedelta(hours=1)
        count = Votacion.objects.filter(fecha_hora__gte=hora_inicio, fecha_hora__lt=hora_fin).count()
        votos_por_hora.append({
            'hora': hora_inicio.strftime('%H:00'),
            'votos': count
        })
    
    return render(request, 'dashboard.html', {
        'total_votos': total_votos,
        'total_candidatos': total_candidatos,
        'total_partidos': total_partidos,
        'votos_por_partido': votos_por_partido,
        'top_candidatos': top_candidatos,
        'votos_recientes': votos_recientes,
        'votos_por_hora': votos_por_hora,
    })