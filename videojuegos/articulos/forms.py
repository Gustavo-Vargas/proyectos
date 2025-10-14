from django import forms
from articulos.models import Articulos
from articulos.models import Categoria

class FormArticulo(forms.ModelForm):
    class Meta:
        model = Articulos
        # fields = ['nombre','genero','stock']
        fields = '__all__'
        # exclude = 'stock'
    

class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'