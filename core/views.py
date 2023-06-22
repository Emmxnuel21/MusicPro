
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect, render
from django.http import Http404
from core.forms import CustomUserCreationForm, productosForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from core.models import productos


def index(request):
    return render(request,'core/index.html')


# SE INICIA VISTA PARA REGISTRO DE USUARIOS

def crearCuenta(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user =authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password2"])
            login(request, user)
            return redirect(to=index)
        data["form"] =formulario
    return render(request, 'registration/register.html', data)

# SE INICIA VISTA PARA PRODUCTOS

@permission_required('core.view_productos')
def bodega(request):

    queryset = request.GET.get("buscar") 
    print(queryset)
    datos=productos.objects.all()
    page = request.GET.get('page',1)
    
    try:
        paginator =Paginator(datos,3)
        datos = paginator.page(page)
    except:
        raise Http404
    
    if queryset:
        
        datos = {
            
            'pacientes':productos.objects.filter(
            Q(idProducto__icontains =queryset)|
            Q(nombreProducto__icontains=queryset)
            ).distinct(),
            'paginator': paginator
        
        }
    else:
        datos = {
            'productos': datos,
            'paginator': paginator
        }
    return render(request, 'core/bodeguero.html',datos)

# PARA PODER AÑADIR PRODUCTOS

@permission_required('core.add_productos')
def form_add_productos(request):
    pro=productosForm()

    datos ={
        'form':pro
    }

    if request.method == 'POST':
        formulario = productosForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, "Paciente Agregado")
            return redirect(to="bodega")
        datos['form'] = pro

    return render(request, 'core/form_pacientes.html',datos)

# PARA PODER MODIFICAR PRODUCTOS

@permission_required('core.change_producto')
def form_mod_productos(request, id):
    pro=productos.objects.get(idProducto=id)
    datos ={
        'form': productosForm(instance=pro)
    }
    if request.method == 'POST':
        formulario = productosForm(data=request.POST,instance=pro)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, "Producto modificado")
            return redirect(to="bodega")
        datos["form"] = formulario
    return render(request, 'core/form_mod_productos.html', datos)

# PARA PODER ELIMINAR PRODUCTOS

@permission_required('core.delete_productos')
def form_del_productos(request, id):
     pro=productos.objects.get(idProducto=id)
     pro.delete()
     messages.success(request, "Producto Eliminado")
     return redirect(to="bodega")

# SE INICIA VISTA PARA VENTAS

@permission_required('core.view_ventas')
def ventas(request):

    queryset = request.GET.get("buscar") 
    print(queryset)
    datos=productos.objects.all()
    page = request.GET.get('page',1)
    
    try:
        paginator =Paginator(datos,3)
        datos = paginator.page(page)
    except:
        raise Http404
    
    if queryset:
        
        datos = {
            
            'pacientes':productos.objects.filter(
            Q(rut__icontains =queryset)|
            Q(nombres__icontains=queryset)
            ).distinct(),
            'paginator': paginator
        
        }
    else:
        datos = {
            'productos': datos,
            'paginator': paginator
        }
    return render(request, 'core/vendedor.html',datos)


# SE INICIA VISTA PARA CONTABILIDAD

@permission_required('core.view_ventas')
def contabilidad(request):

    queryset = request.GET.get("buscar") 
    print(queryset)
    datos=productos.objects.all()
    page = request.GET.get('page',1)
    
    try:
        paginator =Paginator(datos,3)
        datos = paginator.page(page)
    except:
        raise Http404
    
    if queryset:
        
        datos = {
            
            'pacientes':productos.objects.filter(
            Q(rut__icontains =queryset)|
            Q(nombres__icontains=queryset)
            ).distinct(),
            'paginator': paginator
        
        }
    else:
        datos = {
            'productos': datos,
            'paginator': paginator
        }
    return render(request, 'core/vendedor.html',datos)



