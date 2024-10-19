"""
URL configuration for Front project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from FrontApp.views import renderLogin, login,renderRH,  renderMED, salir
from FrontApp.views import renderAdministrador, renderActualizarPaciente, renderRegistrarPaciente,renderBuscaPaciente, renderContactoPaciente, renderPoliza
from FrontApp.views import renderRegistrarEmpleado, renderActualizarEmpleado, renderBuscaEmpleado, renderBuscaEmpleadoN, renderInactivarEmpleado, renderLicenciaEmpleado, renderMuestraEmpleado, renderAsistencias
from FrontApp.views import RegistrarPaciente, RegistrarContacto, BuscarPaciente, ActualizarPaciente, BuscarContactoP, BuscarPacienteP, RegistraPoliza
from FrontApp.views import RegistrarEmpleado, BuscarEmpleado, ActualizarEmpleado, BuscarInactivar, InactivarEmpleado, BuscarEmpleadoN, licenciaEmpleado
from FrontApp.views import renderENF, renderVisita, RegistrarVisita, BuscarVisita, renderbuscaContacto, renderbuscaPoliza
from FrontApp.views import BuscarPacienteH, renderhistoriaClinica, RegistrarHistoriaClinica, BuscarPoliza

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', renderLogin),
    path ('login/', login),   
    path ('login/<id>', salir),
    #rutas para el rol administrador   
    path ('ADM/<id>', renderAdministrador),
    path ('actualizarPaciente/<id>', renderActualizarPaciente),
    path ('registrarPaciente/<id>', renderRegistrarPaciente),
    path ('registrarPaciente1/<id>', RegistrarPaciente),
    path ('actualizarPaciente1/<id>', ActualizarPaciente),
    path ('buscaPaciente/<id>', renderBuscaPaciente),
    path ('buscaPaciente1/<id>', BuscarPaciente),   
    path ('contactoPaciente/<id>', renderContactoPaciente),
    path ('buscaContacto/<id>', renderbuscaContacto),
    path ('contactoPaciente1/<id>', RegistrarContacto),
    path ('buscaContactoP/<id>', BuscarContactoP),
    path ('poliza/<id>', renderPoliza),
    path ('buscaPoliza/<id>', renderbuscaPoliza),
    path ('poliza1/<id>', BuscarPoliza),
    path ('poliza2/<id>', RegistraPoliza),
    #rutas para el rol recursos humanos
    path ('RH/<id>', renderRH),
    path('registrarEmpleado/<id>', renderRegistrarEmpleado),
    path('registrarEmpleado1/<id>', RegistrarEmpleado),
    path('buscaEmpleado/<id>', renderBuscaEmpleado),
    path('buscaEmpleado1/<id>', BuscarEmpleado),    
    path('actualizarEmpleado/<id>', renderActualizarEmpleado),
    path('actualizarEmpleado1/<id>', ActualizarEmpleado),   
    path('inactivarEmpleado/<id>', renderInactivarEmpleado),
    path('inactivarEmpleado1/<id>', BuscarInactivar),
    path('inactivarEmpleado2/<id>', InactivarEmpleado),
    path('buscaEmpleadoN/<id>', renderBuscaEmpleadoN),
    path('buscaEmpleadoN1/<id>', BuscarEmpleadoN),
    path('licenciaEmpleado/<id>', renderLicenciaEmpleado),
    path('licenciaEmpleado1/<id>', licenciaEmpleado),
    path('muestraEmpleado/<id>', renderMuestraEmpleado),
    path('asistencias/<id>', renderAsistencias),
    #ruta para el rol de medico
    path('MED/<id>', renderMED),
    path('historiaClinica/<id>', renderhistoriaClinica),
    path('historiaClinica1/<id>', BuscarPacienteH),
    path('historiaClinica2/<id>', RegistrarHistoriaClinica),
    #ruta para el rol de enfermera
    path ('ENF/<id>', renderENF),
    path('visita/<id>', renderVisita),
    path('visita1/<id>', BuscarVisita),
    path('visita2/<id>', RegistrarVisita)    
]
