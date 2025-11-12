from django import forms
from articulos.models import Articulos
from articulos.models import Categoria
from articulos.models import ArticuloFoto
from django.forms import inlineformset_factory

class FormArticulo(forms.ModelForm):
    class Meta:
        model = Articulos
        # fields = ['nombre','genero','stock']
        fields = '__all__'
        # exclude = 'stock'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }


# class FormCategoria(forms.ModelForm):
#     class Meta:
#         model = Categoria
#         fields = '__all__'

class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        # fields = ['nombre','genero','stock']
        fields = '__all__'
        # exclude = 'stock'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class ArticuloFotoForm(forms.ModelForm):
    class Meta:
        model = ArticuloFoto
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False}),
        }


ArticuloFotoFormSet = inlineformset_factory(
    Articulos,
    ArticuloFoto,
    form=ArticuloFotoForm,
    fields=['imagen'],
    extra=1,
    can_delete=False,
    max_num=10,
)