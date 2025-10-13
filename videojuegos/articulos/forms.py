from django import forms
from articulos.models import Articulos

class FormArticulo(forms.ModelForm):
    class Meta:
        model = Articulos
        # fields = ['nombre','genero','stock']
        fields = '__all__'
        # exclude = 'stock'
    

# class FormEjemplo(forms.Form):
#     pass 
