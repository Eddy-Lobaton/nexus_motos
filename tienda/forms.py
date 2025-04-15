# from django.forms import ModelForm
from django import forms
from .models import TblUsuario

class LoginForm(forms.Form):
    usuario  = forms.CharField(max_length=45, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = TblUsuario
        fields = [
            'usuario_nombreusuario',
            'usuario_password',
            'usuario_nrodocumento',
            'usuario_tipodocumento',
            'usuario_nombre',
            'usuario_paterno',
            'usuario_materno',
            'usuario_fechanac',
            'usuario_email',
            'usuario_sexo',
            'usuario_direccion',
            'tipo_usuario',
            'cargo'
        ]

        labels = {
            'usuario_nombreusuario': 'Nombre de usuario',
            'usuario_password': 'Contraseña',
            'usuario_nrodocumento': 'Número de documento',
            'usuario_tipodocumento': 'Tipo de documento',
            'usuario_nombre': 'Nombre',
            'usuario_paterno': 'Apellido paterno',
            'usuario_materno': 'Apellido materno',
            'usuario_fechanac': 'Fecha de nacimiento',
            'usuario_email': 'Correo electrónico',
            'usuario_sexo': 'Sexo',
            'usuario_direccion': 'Dirección',
            'tipo_usuario': 'Tipo de usuario',
            'cargo': 'Cargo',
        }

        widgets = {
            'usuario_nombreusuario': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'usuario_nrodocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_tipodocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_fechanac': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_email': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_sexo': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'usuario_fechanac': forms.DateInput(attrs={'type': 'date'}),
        }