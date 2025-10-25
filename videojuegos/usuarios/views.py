from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
# from .froms import LoginForm

class LoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    # form_class = LoginForm
    
