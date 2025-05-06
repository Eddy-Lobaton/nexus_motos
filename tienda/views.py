import os
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect

from django.conf import settings
from .forms import LoginForm, RegistroUsuarioForm, ArticuloForm, ProveedorForm, ClienteForm
from .models import TblUsuario, TblProducto, TblProveedor, TblCliente, TblVenta, TblEntrada,TblTipoDocAlmacen, TblDetEntrada
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Max
from django.db import transaction
import json


import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

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

def detalle_articulo(request, producto_id):
    producto = get_object_or_404(TblProducto, pk=producto_id)
    return render(request, 'tienda/detalle_articulo.html', {'producto': producto})

def editar_articulo(request, producto_id):
    producto = get_object_or_404(TblProducto, prod_id=producto_id)

    # Verificamos si el producto tiene una imagen
    tiene_imagen = bool(producto.prod_imagen)

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=producto, tiene_imagen=tiene_imagen)
        
        if form.is_valid():
            producto = form.save(commit=False)
            imagen = request.FILES.get('imagen_archivo')

            if imagen:
                ruta_destino = os.path.join(os.path.dirname(__file__), '..', 'staticfiles', 'tienda', 'img')
                os.makedirs(ruta_destino, exist_ok=True)
                path_final = os.path.join(ruta_destino, imagen.name)
                with open(path_final, 'wb+') as destino:
                    for chunk in imagen.chunks():
                        destino.write(chunk)
                producto.prod_imagen = imagen.name

            producto.save()
            print("Producto editado exitosamente")
            return redirect('lista_articulos')
        else:
            print("Formulario inválido:")
            print(form.errors)
    else:
        form = ArticuloForm(instance=producto, tiene_imagen=tiene_imagen)

    return render(request, 'tienda/editar_articulo.html', {'form': form, 'producto': producto})

@require_POST
def cambiar_estado_articulo(request, producto_id):
    producto = get_object_or_404(TblProducto, prod_id=producto_id)
    producto.prod_estado = not producto.prod_estado
    producto.save()

    estado = "activado" if producto.prod_estado else "desactivado"
    return JsonResponse({"message": f'Artículo "{producto.prod_nombre}" ha sido {estado} correctamente.'})

def lista_proveedores(request):
    proveedor = TblProveedor.objects.all()
    return render(request, 'tienda/lista_proveedores.html', {'proveedor': proveedor})

def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                proveedor = form.save(commit=False)
                proveedor.save()
                return redirect('lista_proveedores')
            except Exception as e:
                print(f'Error al guardar el proveedor: {e}')  # Esto mostrará el error exacto
        else:
            print('Formulario inválido:', form.errors)
    else:
        form = ProveedorForm()

    return render(request, 'tienda/agregar_proveedor.html', {'form': form})

def detalle_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(TblProveedor, pk=proveedor_id)
    return render(request, 'tienda/detalle_proveedor.html', {'detalle_proveedor': proveedor})

def lista_ingresos(request):
    ingresos = TblEntrada.objects.select_related(
        'proveedor', 'tipo_doc_almacen', 'usuario'
    ).all()
    return render(request, 'tienda/lista_ingresos.html', {'ingresos': ingresos})

@transaction.atomic
def agregar_ingresos(request):

    if request.method == "POST":
        try:
            proveedor_id = request.POST.get("proveedor_id")
            tipo_doc_id = request.POST.get("tipo_doc_almacen_id")
            entrada_num_doc = request.POST.get("entrada_num_doc")
            entrada_fecha = request.POST.get("entrada_fecha")
            entrada_igv = float(request.POST.get("entrada_igv", 0))
            entrada_subtotal = float(request.POST.get("subtotal_entrada") or 0)
            entrada_total = float(request.POST.get("total_entrada") or 0)

            articulos_json = request.POST.get("articulos")  # Este será un JSON con los productos
            articulos = json.loads(articulos_json)

            if not articulos:
                messages.error(request, "Debe agregar al menos un producto.")
                return redirect("agregar_ingresos")

            for art in articulos:
                if art["cantidad"] <= 0 or art["precio"] <= 0:
                    messages.error(request, "Cantidad y precio deben ser mayores a cero.")
                    return redirect("agregar_ingresos")

            # Guardar entrada
            entrada = TblEntrada.objects.create(
                entrada_fecha=timezone.now(),  #entrada_fecha,
                entrada_num_doc=entrada_num_doc,
                entrada_subtotal=entrada_subtotal,
                entrada_igv=entrada_igv,
                entrada_costo_total=entrada_total,
                proveedor_id=proveedor_id,
                tipo_doc_almacen_id=tipo_doc_id,
                usuario_id=request.user.id
            )

            # Guardar detalle por producto
            for art in articulos:
                TblDetEntrada.objects.create(
                    entrada=entrada,
                    prod_id=art["id"],
                    det_entrada_cantidad=art["cantidad"],
                    det_entrada_precio_costo=art["precio"],
                    det_entrada_sub_total=art["subtotal"]
                )

            messages.success(request, "Entrada registrada correctamente.")
            return redirect("lista_ingresos")  # Puedes cambiar a la vista de listado

        except Exception as e:
            transaction.set_rollback(True)
            messages.error(request, f"Ocurrió un error: {str(e)}")
            return redirect("agregar_ingresos")

    proveedores = TblProveedor.objects.all()
    tipos_doc = TblTipoDocAlmacen.objects.filter(tipo_doc_almacen_tipo__in=['ES', 'E', 'EI'])
    productos = TblProducto.objects.all()

    tipo_seleccionado_id = request.GET.get('tipo_doc_id')

    if tipo_seleccionado_id:
        tipo_doc = TblTipoDocAlmacen.objects.get(pk=tipo_seleccionado_id)
        tipo_codigo = tipo_doc.tipo_doc_almacen_tipo  # ES, E o EI

        # Lógica de agrupamiento para prefijos y filtrado
        if tipo_codigo in ['ES', 'E']:
            tipo_cod_prefijo = 'E'
            tipos_a_contar = ['ES', 'E']
        elif tipo_codigo == 'EI':
            tipo_cod_prefijo = 'EI'
            tipos_a_contar = ['EI']
        else:
            return JsonResponse({'numero': ''})  # En caso de un tipo inesperado

        # Obtener los tipos que tienen ese tipo_cod_prefijo
        entradas = TblEntrada.objects.filter(
            tipo_doc_almacen__tipo_doc_almacen_tipo__in=tipos_a_contar
        )

        # Extraer el correlativo mayor
        max_num = 0
        for entrada in entradas:
            try:
                num = int(entrada.entrada_num_doc.split("-")[1])
                max_num = max(max_num, num)
            except:
                continue

        nuevo_num = max_num + 1
        numero_generado = f"{tipo_cod_prefijo}-{nuevo_num:05d}"

        return JsonResponse({'numero': numero_generado})


    #hoy = date.today()
    #hace_dos_dias = hoy - timedelta(days=2)

    return render(request, 'tienda/agregar_ingresos.html', {
        'proveedores': proveedores,
        'tipos_doc': tipos_doc,
        'productos': productos,
        #'fecha_hoy': hoy.strftime('%Y-%m-%d'),
        #'fecha_min': hace_dos_dias.strftime('%Y-%m-%d'),
    })

def lista_clientes(request):
    clientes = TblCliente.objects.all()
    return render(request, 'tienda/lista_clientes.html', {'clientes': clientes})

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(TblCliente, pk=cliente_id)
    return render(request, 'tienda/detalle_cliente.html', {'cliente': cliente})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                cliente = form.save(commit=False)
                cliente.save()
                return redirect('lista_clientes')
            except Exception as e:
                print(f'Error al guardar el cliente: {e}')  # Esto mostrará el error exacto
        else:
            print('Formulario inválido:', form.errors)
    else:
        form = ClienteForm()

    return render(request, 'tienda/agregar_cliente.html', {'form': form})

def lista_ventas(request):
    ventas = TblVenta.objects.all()
    return render(request, 'tienda/lista_ventas.html', {'ventas': ventas})

def agregar_venta(request):
    return render(request, 'tienda/agregar_venta.html')

def detalle_venta(request, venta_id):
    venta = get_object_or_404(TblVenta, pk=venta_id)
    return render(request, 'tienda/detalle_venta.html', {'venta': venta})

def lista_usuarios(request):
    usuarios  = TblUsuario.objects.all()
    return render(request, 'tienda/lista_usuarios.html', {'usuarios': usuarios})

def agregar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                usuario.save()
                return redirect('lista_usuarios')
            except Exception as e:
                print(f'Error al guardar el usuario: {e}')  # Esto mostrará el error exacto
        else:
            print('Formulario inválido:', form.errors)
    else:
        form = RegistroUsuarioForm()

    return render(request, 'tienda/agregar_usuario.html', {'form': form})

def detalle_usuario(request, usuario_id):
    usuario = get_object_or_404(TblUsuario, pk=usuario_id)
    return render(request, 'tienda/detalle_usuario.html', {'usuario': usuario})
