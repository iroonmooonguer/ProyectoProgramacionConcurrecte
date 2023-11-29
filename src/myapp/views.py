import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Evento
from datetime import datetime, timedelta


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
                return redirect('home')
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
    eventos = Evento.objects.all()
    return render(request, "pages/eventos.html", {'eventos': eventos})

@login_required
def boleto_vento(request, evento_id) :
    evento = get_object_or_404(Evento, id=evento_id)

    # Puedes acceder al objeto User del usuario autenticado
    usuario = request.user

    nombre = usuario.first_name
    apellido = usuario.last_name

    # Puedes imprimir el nombre y apellido o pasarlos al contexto de renderizado
    # print("Nombre:", nombre)
    # print("Apellido:", apellido)

    return render(request, "pages/boleto_evento.html", {
        'evento': evento,
        'nombre' : nombre,
        'apellido' : apellido
        })

@login_required
def generar_pdf(request) :
    # Obtenemos la información del card desde la solicitud (puedes ajustar esto según tus necesidades)
    ticket_info = {
        'title': request.GET.get('title', ''),
        'organizer': request.GET.get('organizer', ''),
        'date': str(request.GET.get('date', '')),  # Convertir a string
        'time': str(request.GET.get('time', '')),  # Convertir a string
        'nombre': request.GET.get('nombre', ''),
        'apellido': request.GET.get('apellido', ''),
    }

    # Iniciamos un hilo para generar el PDF
    thread = threading.Thread(target=generar_pdf_task, args=(ticket_info,))
    thread.start()

    # Respondemos inmediatamente al usuario
    return HttpResponse("Generación de PDF en progreso. Puedes descargarlo más tarde.")

def generar_pdf_task(ticket_info) :

    # Creamos el objeto HttpResponse con el tipo de contenido PDF.
    response = HttpResponse(generar_pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
    response['Cache-Control'] = 'no-cache'

    # Creamos el objeto PDF, usando el objeto response como su "lienzo".
    p = canvas.Canvas(response)

    # Finalizamos y devolvemos el objeto PDF.
    p.showPage()
    p.save()

    return response
