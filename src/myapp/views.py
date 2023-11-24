from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def iniciar_sesion(request) :
    if request.method == 'GET' :
        return render(request, "pages/iniciar_sesion.html", {
            'form' : AuthenticationForm
        })
    else :
        # Obtener los valores de los campos de nombre de usuario y contraseña del formulario
        username = request.POST['username']
        password = request.POST['password']

        # Validar que los campos no estén vacíos
        if not username or not password:
            return render(request, "pages/iniciar_sesion.html", {
                'form': AuthenticationForm,
                'error': 'Todos los campos son obligatorios'
        })

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None :
            return render(request, "pages/iniciar_sesion.html", {
                'form' : AuthenticationForm,
                'error' : 'El usuario o la contraseña es incorrecto'
            })
        else :
            login(request, user)
            return redirect('dashboard')

def crear_cuenta(request) :
    if request.method == 'GET' :
        return render(request, "pages/crear_cuenta.html", {
            'form' : UserCreationForm
        })
    else :
        # Obtener los valores de los campos del formulario
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']

        # Validar que todos los campos no estén vacíos
        if not (first_name and last_name and email and username and password1 and password2):
            return render(request, "pages/crear_cuenta.html", {
                'form': UserCreationForm,
                'error': 'Todos los campos son obligatorios'
            })

        if request.POST['password1'] == request.POST['password2'] :
            try :
                # Register user
                user = User.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], username = request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except :
                return render(request, "pages/crear_cuenta.html", {
                    'form' : UserCreationForm,
                    'error' : 'El usuario ya existe'
                })
        return render(request, "pages/crear_cuenta.html", {
            'form' : UserCreationForm,
            'error' : 'Las contraseñas no coinciden'
        })

@login_required 
def dashboard(request) :
    return render(request, "pages/dashboard.html", {})

@login_required
def cerrar_sesion(request) :
    logout(request)
    return redirect('home')

@login_required
def mi_perfil(request) :
    return render(request, "pages/perfil.html", {})

@login_required
def eventos(request) :
    return render(request, "pages/eventos.html", {})

@login_required
def boleto_vento(request) :
    return render(request, "pages/boleto_evento.html", {})