from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import DatosPersonales
from django.urls import reverse

class UserForm(forms.ModelForm):
    repassword = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'repassword')
        
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    def clean_password(self, *args, **kwargs):
        if self.data['password'] != self.data['repassword']:
            raise forms.ValidationError('Las contraseñas son diferentes; favor de verificar.')
        return self.data['password']

class FromDatosPersonales(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        # fields ='__all__'
        exclude = ['user']
        
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs['data-url'] = reverse('usuarios:busca_municipios')

# class LoginForm(AuthenticationForm):
    
#     class Meta:
#         fields = '__all__'
        
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }
        
    