"""
URL configuration for clinicaNorbeyAdriana project.

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
from clinicaApp.views import Logueo,UsuarioClinica,Novedades,Asistencias,RegistrarPaciente,ContactoPaciente,Seguro

from clinicaApp.views import ConsultaMedica,ModuloMedicamento,ModuloOrdenMedicamento,ModuloVisitaEnfermera, Procedimiento
from clinicaApp.views import ModuloOrdenProcedimiento, ModuloAyuda, ModuloProcedimiento


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarioClinica',UsuarioClinica.as_view(),name="modulo usuario Recursos Humanos"),
    path('usuarioClinica/<id>',UsuarioClinica.as_view(),name="Busca_empleado"),
    path('novedades',Novedades.as_view(),name="modulo Novedades de usuario Recursos Humanos"),
    path('novedades/<id>',Novedades.as_view(),name="modulo usuario Recursos Humanos"),
    path('asistencias',Asistencias.as_view(),name="modulo Novedades de usuario Recursos Humanos"),
    path('asistencias/<id>',Asistencias.as_view(),name="modulo usuario Recursos Humanos"),
    path('paciente', RegistrarPaciente.as_view(), name='modulo paciente'), 
    path('paciente/<id>', RegistrarPaciente.as_view(), name='modulo paciente'), 
    path('contactoPaciente', ContactoPaciente.as_view(), name='modulo paciente contacto'), 
    path('contactoPaciente/<id>', ContactoPaciente.as_view(), name='modulo paciente contacto'), 
    path('contactoPaciente/paciente/<cc>', ContactoPaciente.as_view(), name='modulo paciente contacto'), 
    path('seguropaciente', Seguro.as_view(), name='modulo paciente Seguro'), 
    path('seguropaciente/<id>', Seguro.as_view(), name='modulo paciente Seguro'),   
    path('medicamento', ModuloMedicamento.as_view(), name='modulo Medico Mediicamento'), 
    path('medicamento/<id>', ModuloMedicamento.as_view(), name='modulo Medico Mediicamento'),
    path('procedimiento', ModuloProcedimiento.as_view(), name='moduloprocedimientos'), 
    path('procedimiento/<id>', ModuloProcedimiento.as_view(), name='moduloprocedimientos'),
    path('ayuda', ModuloAyuda.as_view(), name='ayudas'),
    path('ayuda/<id>', ModuloAyuda.as_view(), name='ayudas'),
    path('ordenmedicamento', ModuloOrdenMedicamento.as_view(), name='Modulo ModuloOrdenMedicamento'), 
    path('ordenmedicamento/<id>', ModuloOrdenMedicamento.as_view(), name='Modulo ModuloOrdenMedicamento'), 
    path('ordenmedicamento/paciente/<cc>', ModuloOrdenMedicamento.as_view(), name='Modulo ModuloOrdenMedicamento'), 
    path('ordenmedicamento/<id>/<cc>', ModuloOrdenMedicamento.as_view(), name='modulo Medico Mediicamento'), 
    path('ordenprocedimiento/<id>', ModuloOrdenProcedimiento.as_view(), name='ordenprocedimiento'),
    path('ordenprocedimiento/paciente/<cc>', ModuloOrdenProcedimiento.as_view(), name='ordenprocedimiento'),
    path('consulta', ConsultaMedica.as_view(), name='modulo Medico HistoriaClinica'), 
    path('consulta/<id>', ConsultaMedica.as_view(), name='modulo  Medico HistoriaClinica'), 
    path('visita', ModuloVisitaEnfermera.as_view(), name='modulo  Visita Enfermera'), 
    path('logueo',Logueo.as_view(),name='login'),
    path ('salir',Logueo.as_view(),name='salir')
]
