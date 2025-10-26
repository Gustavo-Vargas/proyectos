from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
# from .froms import LoginForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import UserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class LoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    # form_class = LoginForm
    
class RegistrarView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_mesage = "%(username)s se ha registrado de manera exitosa"

    