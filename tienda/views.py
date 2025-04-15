from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroUsuarioForm
from .models import TblUsuario
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')


def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            usuarios = form.cleaned_data['usuario']
            passwords = form.cleaned_data['password']

            # Buscar el usuario en la base de datos
            try:
                user = TblUsuario.objects.get(usuario_nombreusuario=usuarios)

                # Verificar la contraseña
                if user.usuario_password == passwords:  # Asumiendo que la contraseña está almacenada en texto claro (no recomendado)
                    # Autenticación exitosa, iniciar sesión
                    # Puedes almacenar el id del usuario en la sesión de Django
                    request.session['usuario_id'] = user.usuario_id
                    return redirect('home')  # Redirigir a la página de inicio (puedes cambiarla por la vista que desees)
                else:
                    form.add_error('password', 'Contraseña incorrecta')
            except TblUsuario.DoesNotExist:
                form.add_error('usuario', 'El nombre de usuario no existe')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login')  # o a donde quieras redirigir después
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})
