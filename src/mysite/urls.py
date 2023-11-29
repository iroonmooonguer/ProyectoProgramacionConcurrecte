"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.iniciar_sesion, name='home'),
    path('signup', views.crear_cuenta, name='signup'),
    path('logout', views.cerrar_sesion, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('my-profile', views.mi_perfil, name='perfil'),
    path('events', views.eventos, name='eventos'),
    path('ticket_event/<int:evento_id>/', views.boleto_vento, name='ticket'),
    path('generar_pdf', views.generar_pdf, name='generar_pdf'),
    path('admin/', admin.site.urls)
]

if settings.DEBUG :
    # do not do this in prod
    from django.conf.urls.static import static
    #try django
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
