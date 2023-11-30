from pymongo import MongoClient
import threading
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Evento


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
    doc = SimpleDocTemplate("ticket.pdf", pagesize=letter)
    elementos = []

    # Estilo para los párrafos
    estilos = getSampleStyleSheet()

    # Obtenemos la información del card desde la solicitud
    ticket_info = {
        'Evento': request.GET.get('title', ''),
        'Organizador': request.GET.get('organizer', ''),
        'Fecha': str(request.GET.get('date', '')),  # Convertir a string
        'Hora': str(request.GET.get('time', '')),  # Convertir a string
        'Nombre': request.GET.get('nombre', ''),
        'Apellido': request.GET.get('apellido', ''),
    }

    # Crear una tarjeta para la información del ticket
    tarjeta = [
        Paragraph(f"<b>{clave}:</b> {valor}", estilos['BodyText']) for clave, valor in ticket_info.items()
    ]

    elementos.extend(tarjeta)
    elementos.append(Spacer(1, 12))  # Espaciador entre tarjetas
    doc.build(elementos)


    pdf = open('ticket.pdf', 'rb')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

    return response 
    return render(request, "pages/dashboard.html", {
        'alerta' : 'Boleto virtual descargado correctamente'
    })

# Función para realizar la consulta a la base de datos MongoDB
def consultar_base_de_datos():
    try:
        # Conectar a la base de datos MongoDB (ajusta la URL y otros parámetros según tu configuración)
        client = MongoClient('mongodb+srv://root:qHMEGeaehFj8a0D7@cluster0.px2sqnh.mongodb.net/test')
        db = client['hgowebcampo']
        collection = db['myapp_evento']

        # Realizar la consulta a MongoDB (cambia esto según tu consulta)
        consulta = collection.find({})
        datos = list(consulta)

        client.close()

        if datos:
            # Llamar a la función para generar el informe PDF
            generar_pdf(datos)
            print("Informe PDF generado con éxito.")
        else:
            print("No se encontraron datos en la consulta.")

    except Exception as e:
        print(f"Error al conectar a la base de datos: {str(e)}")

# Utilizar hilos para la consulta y generación de informe
hilo_consulta = threading.Thread(target=consultar_base_de_datos)
hilo_consulta.start()
hilo_consulta.join()