from django import forms
from votos.models import Partido, Candidato

class PartidoForm(forms.ModelForm):
    
    class Meta:
        model = Partido
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CandidatoForm(forms.ModelForm):
    
    class Meta:
        model = Candidato
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ap_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'ap_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'partido': forms.Select(attrs={'class': 'form-control'}),
        }
