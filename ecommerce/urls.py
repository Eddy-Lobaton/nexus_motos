"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registrar/api/consultar-dni/', views.consultar_dni, name='consultar_dni'),
    path('registrar/verificar-username/', views.verificar_username, name='verificar_username'),
    path('registrar/verificar-datos-bd/', views.verificar_datos, name='verificar_datos'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('logout/',views.signoup, name= 'logout'),
    path('productos/',views.lista_productos, name= 'lista_productos'),
    path('articulos/',views.lista_articulos, name= 'lista_articulos'),
    path('agregar_articulos/',views.agregar_articulos, name= 'agregar_articulos'),
    path('lista_proveedores/',views.lista_proveedores, name= 'lista_proveedores'),
    path('agregar_proveedor/',views.agregar_proveedor, name= 'agregar_proveedor'),
]
