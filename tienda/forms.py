# from django.forms import ModelForm
from django import forms
from .models import TblUsuario, TblProducto
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta


class LoginForm(forms.Form):
    usuario  = forms.CharField(max_length=45, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# Opciones para tipo de documento
TIPO_DOCUMENTO_OPCIONES = [
    ('', 'Seleccionar...'),
    ('DNI', 'DNI'),
    ('CE', 'Carnet de extranjería'),
]
SEXO = [
    ('', 'Seleccionar...'),
    ('FEMENINO', 'Femenino'),
    ('MASCULINO', 'Masculino'),
]

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = TblUsuario
        fields = [
            'usuario_tipodocumento',
            'usuario_nrodocumento',
            'usuario_nombre',
            'usuario_paterno',
            'usuario_materno',
            'usuario_direccion',           
            'usuario_fechanac',
            'usuario_sexo',
            'usuario_email',
            'cargo',
            'tipo_usuario',
            'username',
            'password'
        ]

        labels = {
            'usuario_tipodocumento': 'Tipo de documento',
            'usuario_nrodocumento': 'Número de documento',
            'usuario_nombre': 'Nombre',
            'usuario_paterno': 'Apellido paterno',
            'usuario_materno': 'Apellido materno',
            'usuario_direccion': 'Dirección',
            'usuario_fechanac': 'Fecha de nacimiento',
            'usuario_sexo': 'Sexo',
            'usuario_email': 'Correo electrónico',
            'cargo': 'Cargo',
            'tipo_usuario': 'Tipo de usuario',
            'username': 'Nombre de usuario',
            'password': 'Contraseña'
        }

        widgets = {
            'usuario_tipodocumento': forms.Select(choices=TIPO_DOCUMENTO_OPCIONES, attrs={'class': 'form-control'}),
            'usuario_nrodocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_fechanac': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'usuario_sexo': forms.Select(choices=SEXO, attrs={'class': 'form-control'}),
            'usuario_email': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cambiar la etiqueta por defecto
        self.fields['tipo_usuario'].empty_label = "Seleccionar..."
        self.fields['cargo'].empty_label = "Seleccionar..."

        # Rango de año para fecha de nacimiento
        hoy = date.today()
        edad_min = hoy.replace(year=hoy.year - 70)
        edad_max = hoy.replace(year=hoy.year - 18)
        self.fields['usuario_fechanac'].widget.attrs['min'] = edad_min.isoformat()
        self.fields['usuario_fechanac'].widget.attrs['max'] = edad_max.isoformat()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class ArticuloForm(forms.ModelForm):
    imagen_archivo = forms.FileField(
        required=False,  # El requerido lo manejamos manualmente en clean()
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = TblProducto
        fields = ['prod_nombre', 'prod_marca', 'prod_modelo', 'prod_motor', 'prod_categoria', 'prod_descripcion']
        widgets = {
            'prod_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'prod_marca': forms.TextInput(attrs={'class': 'form-control'}),
            'prod_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'prod_motor': forms.TextInput(attrs={'class': 'form-control'}),
            'prod_categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'prod_descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Aquí se determina si el producto ya tiene imagen, para luego decidir si la imagen es obligatoria
        self.tiene_imagen = kwargs.pop('tiene_imagen', False)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        imagen = self.files.get('imagen_archivo')

        # Si no tiene imagen previa y no se sube una nueva, lanzar error
        if not self.tiene_imagen and not imagen:
            self.add_error('imagen_archivo', 'Debes subir una imagen.')

        return cleaned_data
