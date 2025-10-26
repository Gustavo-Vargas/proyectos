from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    

# class LoginForm(AuthenticationForm):
    
#     class Meta:
#         fields = '__all__'
        
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }
        
    