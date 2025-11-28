from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse

from .models import DatosPersonales
from .forms import FromDatosPersonales, UserForm
from .token import token_activacion

class ListaUsuariosView(ListView):
    model = User
    template_name = 'lista_usuarios.html'
    
    def get_context_data(self, **kwargs):
        context = super(ListaUsuariosView, self).get_context_data(**kwargs)    
        context['grupos'] = Group.objects.all()
        return context
    
        # kwargs.setdefault("view", self)
        # if self.extra_context is not None:
        #     kwargs.update(self.extra_context)
        # return kwargs

def asignar_grupos(request):
    id_usuario = request.POST.get('usuario', None)
    
    if not id_usuario or id_usuario == '':
        messages.error(request, 'No se seleccionó un usuario')
        return redirect('usuarios:lista')
    
    try:
        usuario = User.objects.get(id=int(id_usuario))
    except (ValueError, User.DoesNotExist):
        messages.error(request, 'Usuario no encontrado')
        return redirect('usuarios:lista')
    
    usuario.groups.clear()
    for item in request.POST:
        if item != 'usuario' and item != 'csrfmiddlewaretoken' and request.POST[item] == 'on':
            try:
                grupo = Group.objects.get(id=int(item))
                usuario.groups.add(grupo)
            except (ValueError, Group.DoesNotExist):
                continue
    
    messages.success(request, 'Se agregó el usuario a los grupos')
        
    return redirect('usuarios:lista')

class LoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    # form_class = LoginForm
    
class RegistrarView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('usuarios:login')
    success_message = "%(username)s se ha registrado de manera exitosa"
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        sitio = get_current_site(self.request)
        
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string(
            'confirmar_cuenta.html',
            {
                'user': user,
                'sitio': sitio,
                'uid': uid,
                'token': token
            }
        )
        
        asunto = 'Activar cuenta'
        para = user.email
        email = EmailMessage(
            asunto,
            mensaje,
            to=[para],
        )
        email.content_subtype = 'html'
        email.send()
        
        return super().form_valid(form)
    
class ActivarCuentaView(TemplateView):
    def get(self, request, *args, **kwargs):
        
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']) 
            token = kwargs['token']
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, User.DoesNotExist):
           user = None
        
        if user is not None and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            
            messages.success(request, 'Cuenta activada, ingresar datos')
        
        else:
            messages.error(request, 'Token invalido, contacta al administrador')
        
        return redirect('usuarios:login')
        

class CrearPerfilView(SuccessMessageMixin, CreateView):
    model = DatosPersonales
    form_class = FromDatosPersonales
    success_url = reverse_lazy('bienvenida')
    success_message = "Se guardaron tus datos personales"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.request.user, 'datos'):
            kwargs['instance'] = self.request.user.datos
        return kwargs

    def form_valid(self, form):
        datos_personales = form.save(commit=False)
        if not datos_personales.pk:
            datos_personales.user = self.request.user
        if datos_personales.pk:
            anterior = DatosPersonales.objects.get(pk=datos_personales.pk)
            if anterior.foto and form.cleaned_data.get('foto') and anterior.foto.name != form.cleaned_data['foto'].name:
                anterior.foto.delete(save=False)
        datos_personales.save()
        
        return super().form_valid(form)
        
    