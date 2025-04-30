import os
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.conf import settings
from .forms import LoginForm, RegistroUsuarioForm, ArticuloForm
from .models import TblUsuario, TblProducto
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime

import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'tienda/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            usuarios = form.cleaned_data['usuario']
            passwords = form.cleaned_data['password']

            # Buscar el usuario de forma segura
            user_qs = TblUsuario.objects.filter(username=usuarios)  #obtiene todos los registros que coinciden con el username
            if user_qs.exists():
                if user_qs.count() > 1:
                    form.add_error('usuario', 'Hay múltiples usuarios con este nombre. Contacta al administrador.')
                else:
                    # Intentamos autenticar (validar contraseña)
                    user = authenticate(request, username=usuarios, password=passwords)
                    if user is not None:
                        login(request, user)
                        request.session['id'] = user.id     # Puedes usar user.usuario_id si lo prefieres
                        return redirect('home')
                    else:
                        form.add_error('password', 'Contraseña incorrecta') # Añadir error para la contraseña incorrecta
                        #form.add_error(None, 'Contraseña incorrecta')
            else:
                form.add_error('usuario', 'El nombre de usuario no existe')
    else:
        form = LoginForm()

    return render(request, 'tienda/login.html', {'form': form})


@require_GET
def consultar_dni(request):
    dni = request.GET.get('dni')
    if not dni:
        return JsonResponse({'success': False, 'error': 'DNI no proporcionado.'})
    
    try:
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzODU0MiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.-e-nfoCiwEwPqJrbjNzNRQHhlzm21LIAolTMsTcTZEE'
        url = f"https://api.factiliza.com/v1/dni/info/{dni}"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        #print(response.text)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse({
                'success': True,
                'nombres': data.get('data', {}).get('nombres'), #data['data']['nombres']
                'apellido_paterno': data.get('data', {}).get('apellido_paterno'),
                'apellido_materno': data.get('data', {}).get('apellido_materno'),
                'direccion': data.get('data', {}).get('direccion'),
            })
        else:
            return JsonResponse({'success': False, 'error': 'DNI no encontrado.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_GET
def verificar_username(request):
    username = request.GET.get('username', '')
    existe = User.objects.filter(username=username).exists()
    return JsonResponse({'existe': existe})

def verificar_datos(request):
    numDoc = request.GET.get('numDoc')
    email = request.GET.get('email')
    existeDoc = TblUsuario.objects.filter(usuario_nrodocumento=numDoc).exists() if numDoc else False
    existeEmail = TblUsuario.objects.filter(usuario_email=email).exists() if email else False

    return JsonResponse({'existsDoc': existeDoc, 'existsEmail': existeEmail})


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
    return render(request, 'tienda/registro.html', {'form': form})

def signoup (request):
    logout(request) 
    return redirect('home')

def lista_productos(request):
    productos = TblProducto.objects.all()
    paginator = Paginator(productos, 6)  # Mostrar 6 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tienda/productos.html', {'page_obj': page_obj})

def lista_articulos(request):
    productos = TblProducto.objects.all()
    return render(request, 'tienda/lista_articulos.html', {'productos': productos})


def agregar_articulos(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                producto = form.save(commit=False)
                imagen = request.FILES.get('imagen_archivo')

                if imagen:
                    ruta_destino = os.path.join(settings.BASE_DIR, 'staticfiles', 'tienda', 'img')
                    os.makedirs(ruta_destino, exist_ok=True)
                    path_final = os.path.join(ruta_destino, imagen.name)

                    with open(path_final, 'wb+') as destino:
                        for chunk in imagen.chunks():
                            destino.write(chunk)

                    producto.prod_imagen = imagen.name  # solo el nombre del archivo

                producto.prod_fecha_registro = datetime.now()
                producto.save()
                return redirect('lista_articulos')
            except Exception as e:
                print(f'Error al guardar el producto: {e}')  # Esto mostrará el error exacto
        else:
            print('Formulario inválido:', form.errors)
    else:
        form = ArticuloForm()

    return render(request, 'tienda/agregar_articulos.html', {'form': form})


def lista_proveedores(request):
    return render(request, 'tienda/lista_proveedores.html')

def agregar_proveedor(request):
    return render(request, 'tienda/agregar_proveedor.html')

def lista_ingresos(request):
    return render(request, 'tienda/lista_ingresos.html')

def agregar_ingresos(request):
    return render(request, 'tienda/agregar_ingresos.html')

def lista_clientes(request):
    return render(request, 'tienda/lista_clientes.html')

def agregar_cliente(request):
    return render(request, 'tienda/agregar_cliente.html')

