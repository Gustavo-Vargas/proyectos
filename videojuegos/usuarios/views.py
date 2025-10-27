from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
# from .froms import LoginForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import FromDatosPersonales, UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import DatosPersonales


class LoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    # form_class = LoginForm
    
class RegistrarView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = "%(username)s se ha registrado de manera exitosa"

class CrearPerfilView(SuccessMessageMixin, CreateView):
    model = DatosPersonales
    form_class = FromDatosPersonales
    success_url = reverse_lazy('bienvenida')
    success_message = "Se guardaron tus datos personales"
    
    def form_valid(self, form):
        datos_personales = form.save(commit=False)
        datos_personales.user = self.request.user
        datos_personales.save()
        
        return super().form_valid(form)
        
    
