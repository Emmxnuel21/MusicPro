
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect, render
from django.http import Http404
from core.forms import CustomUserCreationForm, productosForm, ventasForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import productos ,ventas
import random
from django.urls import reverse
from django.views.decorators.http import require_GET
from transbank.webpay.webpay_plus.transaction import Transaction




def index(request):
    return render(request,'core/index.html')


def accesorios(request):
    return render(request,'core/accesorios.html')



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

@permission_required('auth.ser_bode')
def bodega(request):

    queryset = request.GET.get("buscar") 
    print(queryset)
    datos=productos.objects.all()
    page = request.GET.get('page',1)
    
    try:
        paginator =Paginator(datos,10)
        datos = paginator.page(page)
    except:
        raise Http404
    
    if queryset:
        
        datos = {
            
            'productos':productos.objects.filter(
            Q(serie__icontains =queryset)|
            Q(nombre__icontains=queryset)
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

@permission_required('auth.ser_bode')
def form_add_productos(request):
    pro=productosForm()

    datos ={
        'form':pro
    }

    if request.method == 'POST':
        formulario = productosForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, "Producto Agregado")
            return redirect(to="bodega")
        datos['form'] = pro

    return render(request, 'core/form_add_productos.html',datos)

# PARA PODER MODIFICAR PRODUCTOS

@permission_required('auth.ser_bode')
def form_mod_productos(request, id):
    pro=productos.objects.get(serie=id)
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

@permission_required('auth.ser_bode')
def form_del_productos(request, id):
     pro=productos.objects.get(serie=id)
     pro.delete()
     messages.success(request, "Producto Eliminado")
     return redirect(to="bodega")

# SE INICIA VISTA PARA VENTAS

@permission_required('auth.ser_vend')
def vendedor(request):

    queryset = request.GET.get("buscar") 
    print(queryset)
    datos=ventas.objects.all()
    page = request.GET.get('page',1)
    
    try:
        paginator =Paginator(datos,5)
        datos = paginator.page(page)
    except:
        raise Http404
    
    if queryset:
        
        datos = {
            
            'ventas':ventas.objects.filter(
            Q(idVenta__icontains =queryset)|
            Q(productosVendidos__icontains=queryset)
            ).distinct(),
            'paginator': paginator
        
        }
    else:
        datos = {
            'ventas': datos,
            'paginator': paginator
        }
    return render(request, 'core/vendedor.html',datos)

# SE INICIA VISTA PARA CONTABILIDAD

@permission_required('auth.ser_conta')
def contabilidad(request):

    queryset = request.GET.get("buscar") 
    print(queryset)
    datos=ventas.objects.all()
    page = request.GET.get('page',1)
    
    try:
        paginator =Paginator(datos,10)
        datos = paginator.page(page)
    except:
        raise Http404
    
    if queryset:
        
        datos = {
            
            'ventas':ventas.objects.filter(
            Q(idVenta__icontains =queryset)|
            Q(productosVendidos__icontains=queryset)
            ).distinct(),
            'paginator': paginator
        
        }
    else:
        datos = {
            'ventas': datos,
            'paginator': paginator
        }
    return render(request, 'core/contador.html',datos)

# PARA PODER AÑADIR VENTAS CONTABILIDAD

@permission_required('auth.ser_conta')
def form_add_ventas(request):
    ven=ventasForm()

    datos ={
        'form':ven
    }

    if request.method == 'POST':
        formulario = ventasForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, "Venta Agregada")
            return redirect(to="contabilidad")
        datos['form'] = ven

    return render(request, 'core/form_add_ventas.html',datos)

# SE CREA PARA MODIFICAR VENTAS CONTABILIDAD

@permission_required('auth.ser_conta')
def form_mod_ventas(request, id):
    ven=ventas.objects.get(idVenta=id)
    datos ={
        'form': ventasForm(instance=ven)
    }
    if request.method == 'POST':
        formulario = ventasForm(data=request.POST,instance=ven)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, "Venta Modificado")
            return redirect(to="contabilidad")
        datos["form"] = formulario
    return render(request, 'core/form_mod_ventas.html', datos)

# SE CREA PARA PODER ELIMINAR VENTAS

@permission_required('auth.ser_conta')
def form_del_ventas(request, id):
     ven=ventas.objects.get(idVenta=id)
     ven.delete()
     messages.success(request, "Venta Eliminada")
     return redirect(to="contabilidad")

# SE GENERAN VISTA PARA LA SECCION DE COMPRAS DE NUESTRA WEB JUNTO CON LA REEDIRECCION A TRANSBANK PARA LOS PAGOS

@require_GET
def guitarras(request):
    queryset = request.GET.get("buscar") 
    print(queryset)
    datos = productos.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(datos, 10)
        datos = paginator.page(page)
    except:
        raise Http404

    if queryset:
        datos = {
            'productos': productos.objects.filter(
                Q(serie__icontains=queryset) |
                Q(nombre__icontains=queryset)
            ).distinct(),
            'paginator': paginator
        }
    else:
        datos = {
            'productos': datos,
            'paginator': paginator
        }

    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 500000)
    return_url = request.build_absolute_uri(reverse('commit'))

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = Transaction().create(buy_order, session_id, amount, return_url)

    print(response)

    context = {
        'request': create_request,
        'response': response,
        'productos': datos['productos'],
        'paginator': datos['paginator'],
    }

    return render(request, 'core/guitarras.html', context)





def webpay_plus_commit(request):
    token = request.GET.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = Transaction().commit(token=token)
    print("response: {}".format(response))

    context = {'token': token, 'response': response}  

    return render(request, 'core/commit.html', context)  


