from django import forms
from votos.models import Partido

class PartidoForm(forms.ModelForm):
    
    class Meta:
        model = Partido
        fields = '__all__'

