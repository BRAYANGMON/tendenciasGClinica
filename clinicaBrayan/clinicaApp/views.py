from datetime import datetime,date
from typing import Any
from django import http
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import PersonalClinica,Sesion,Asistencia, Paciente
from .models import Novedad,informaContacto,SeguroPaciente,Medicamento,OrdenMedicamento,Orden,Procedimiento,OrdenProcedimiento,OrdenAyudaDiagnostica
from .models import VisitaEnfermera, Ayuda
from clinicaNorbeyAdriana.conexionMongo import collection
import json,secrets,string
from .helpers import validadorGeneral, validadorPersonalClinica, controlPacientes, validadorNovedades,validadorEnfermeras, controlSeguros, controlFacturas, validadorOrdenes
from .helpers import controlOrdenes, controlPersonalClinica, validadorMedicos
from django.db.models import Max
# Create your views here.

def validarRol(sesion,rol):
    print(sesion.usuario.nombre)
    if sesion.usuario.rol not in rol and sesion.usuario.usuario!="Andres":
        raise Exception("el usuario no posee permisos")
    
class Logueo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        #login = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            #validarRol(sesion,["ADM"])
            rol=sesion.usuario.rol
            status=200
            message = "paso la validacion"
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "rol": rol}
        return JsonResponse(response,status=status) 

    def put(self,request):
        pass

    def post(self, request):
        token=""
        message=""
        try:
            body = json.loads(request.body)
            rol = body["rol"]
            usuario=body["usuario"]
            password=body["contraseña"]
            personalClinica = PersonalClinica.objects.get(usuario=usuario,rol=rol,password=password,estado=1)
            sesion = Sesion.objects.filter(usuario=personalClinica)
            if sesion.exists():
                raise Exception("El usuario ya esta en sesion")
            caracteres = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(caracteres) for _ in range(128))
            sesion = Sesion(usuario=personalClinica,token=token)
            
            sesion.save()
            message += "Login Exitoso"
#logica de asistencia
            try:
                tipo = "asistencia"
                #Falta validar que la asistencia solo filtre la del dia actual
                fechaAsistencia = date.today().strftime('%Y-%m-%d')
                asistencia = Asistencia.objects.filter(cedula=personalClinica,fechaRegistro=fechaAsistencia)
                if asistencia.exists():
                    raise Exception("El usuario ya registro Asistencia")
                asistencia = Asistencia(tipo=tipo,cedula=personalClinica,fechaRegistro=fechaAsistencia)
                asistencia.save()
                message+=" registro de asistencia exitoso"
                status = 200
            except Exception as error:
                message += str(error)
                status = 200
        except Exception as error:
            message += str(error)
            status = 400
        response = {"message": message, "token":token}
        return JsonResponse(response,status=status)

    def delete(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            sesion.delete()
            message="se ha cerrado sesion"
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)   

class UsuarioClinica(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        personalClinica = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            if id:
                personalClinica = list(PersonalClinica.objects.filter(cedula=id,estado=1).values())
            else:
                personalClinica = list(PersonalClinica.objects.values())
            print(personalClinica)    
            if len(personalClinica)>0:
                message = "registros encontrados"
            else:
                message="registros Personal clinica no encontrados"
                status = 400
                raise Exception("Registros Personal clinica no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Empleados": personalClinica}
        return JsonResponse(response,status=status)
    
    def put(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            cedula = body["cedula"]
            email = body["email"]
            telefono = body["telefono"]
            fecha_nacimiento = body["fechanace"]
            direccion = body["direccion"]
            rol = body["rol"]
            usuario = body["usuario"]
            password = body["password"]
            validadorGeneral.validarNombre(nombre)
            #validadorGeneral.validarCedula(cedula)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validar_fecha(fecha_nacimiento)
            validadorPersonalClinica.validarDatosUsuario(rol,usuario,password)
            validadorGeneral.ValidarPassword(password)
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            empleado_Actualizado = PersonalClinica.objects.get(cedula=cedula)
            empleado_Actualizado.nombre = nombre
            empleado_Actualizado.email = email
            empleado_Actualizado.fecha_nacimiento = fecha_nacimiento
            empleado_Actualizado.direccion = direccion
            empleado_Actualizado.rol = rol
            empleado_Actualizado.usuario = usuario
            empleado_Actualizado.password = password
            empleado_Actualizado.save()
            message = "usuario Actualizado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            cedula = body["cedula"]
            email = body["email"]
            telefono = body["telefono"]
            fecha_nacimiento = body["fechanace"]
            direccion = body["direccion"]
            rol = body["rol"]
            usuario = body["usuario"]
            password = body["password"]
            
            validadorGeneral.validarNombre(nombre)
            validadorGeneral.validarCedula(cedula)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validar_fecha(fecha_nacimiento)
            validadorPersonalClinica.validarDatosUsuario(rol,usuario,password)
            validadorGeneral.ValidarPassword(password)
            empleado_new = PersonalClinica.objects.filter(cedula=cedula)
            if empleado_new.exists():
                raise Exception("Ya Existe un empleado registrado con esa Cedula")
            empleado_new = PersonalClinica.objects.filter(usuario=usuario)
            if empleado_new.exists():
                raise Exception("Ya Existe un empleado registrado con ese Usuario")
            
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            empleado_new = PersonalClinica(nombre=nombre,cedula=cedula,email=email,telefono=telefono,fecha_nacimiento=fecha_nacimiento,direccion=direccion,rol=rol,usuario=usuario,password=password,estado=1)
            empleado_new.save()
            message = "usuario Registrado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

            
    def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])   
            empleado_Eliminado = PersonalClinica.objects.get(cedula=id)
            empleado_Eliminado.estado = 0
            empleado_Eliminado.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status)
  
class Novedades(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        novedades = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            if id:
                novedades = list(Novedad.objects.filter(idNovedad=id).values())
            else:
                novedades = list(Novedad.objects.values())
                
            if len(novedades)>0:
                message = "registros encontrados"
            else:
                message="registros de novedades no encontrados"
                status = 400
                raise Exception("Registros de novedades no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Novedades": novedades}
        return JsonResponse(response,status=status)
    
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            body = json.loads(request.body)
            tipo = body["tipo"]
            cedula = body["cedula"]
            tiempo = body["tiempo"]
            fechaRegistro = body["fechaRegistro"]
            observaciones = body["observaciones"]
            validadorGeneral.validarCedula(cedula)
            validadorNovedades.TipoNovedad(tipo)
            validadorNovedades.ValidarTiempo(tiempo)
            validadorGeneral.validar_fecha(fechaRegistro)

            empleado = PersonalClinica.objects.get(cedula=cedula)
            #if empleado_new.exists():
            #    raise Exception("Ya Existe un empleado registrado con esa Cedula")
            #empleado_new = PersonalClinica.objects.filter(usuario=usuario)
            #if empleado_new.exists():
            #    raise Exception("Ya Existe un empleado registrado con ese Usuario") 
            
            dd, mm, yyy = fechaRegistro.split('/')
            fechaRegistro = f"{yyy}-{mm}-{dd}"
            novedad_new = Novedad(tipo=tipo,cedula=empleado,tiempo=tiempo,fechaRegistro=fechaRegistro,observaciones=observaciones)
            novedad_new.save()
            
            message = "Novedad Registrada Registrado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)
    
    def put(self,request):
        pass
    def delete(self,request):
        pass

class Asistencias(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        asistenciasEmpleados = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            if id:
                asistenciasEmpleados = list(Asistencia.objects.filter(idNovedad=id).values())
            else:
                asistenciasEmpleados = list(Asistencia.objects.values())
                print(asistenciasEmpleados)
                for asistencia in asistenciasEmpleados:
                    empleado=PersonalClinica.objects.get(cedula=asistencia["cedula_id"])
                    asistencia["nombre"]=empleado.nombre
                    asistencia["rol"]=empleado.rol
                print(asistenciasEmpleados)
            if len(asistenciasEmpleados)>0:
                message = "registros encontrados"
            else:
                message="registros de Asistencias no encontrados"
                status = 400
                raise Exception("Registros de Asistencias no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Asistencias": asistenciasEmpleados}
        return JsonResponse(response,status=status)
    
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["RH"])
            body = json.loads(request.body)
            tipo = "Asistencia"
            cedula = body["cedula"]
            fechaAsistencia = date.today().strftime('%Y-%m-%d')
            validadorGeneral.validarCedula(cedula)

            empleado = PersonalClinica.objects.get(cedula=cedula)
            asistencia = Asistencia.objects.filter(cedula=empleado,fechaRegistro=fechaAsistencia)
            if asistencia.exists():
                    raise Exception("El usuario ya registro Asistencia")

            asistencia = Asistencia(tipo=tipo,cedula=empleado,fechaRegistro=fechaAsistencia)
            asistencia.save()
            message=" registro de asistencia exitoso"
            status = 200
            
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class RegistrarPaciente(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        pacientes = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM","MED","ENF"])
            if id:
                pacientes = list(Paciente.objects.filter(cedula=id,estado=1).values())
            else:
                pacientes = list(Paciente.objects.values())
                
            if len(pacientes)>0:
                message = "Pacientes no encontrados"
            else:
                message="Pacientes no encontrados"
                status = 400
                raise Exception("Pacientes no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Pacientes": pacientes}
        return JsonResponse(response,status=status)

    def put(self,request):
        pacienteActualizado=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            body=json.loads(request.body)
            cedula=body["cedula"]            
            #actualizar datos
            pacienteActualizado = Paciente.objects.get(cedula=cedula)
            nombre = body["nombre"]
            genero = body["genero"]            
            fecha_nacimiento = body["fechanace"]            
            telefono = body["telefono"]
            direccion = body["direccion"]           
            email = body["email"]
            validadorGeneral.validarNombre(nombre)
            validadorGeneral.validarGenero(genero)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validar_fecha(fecha_nacimiento) 
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            #pacienteActualizado = Paciente(nombre,cedula,fecha_nacimiento, genero, direccion, email, telefono)
            pacienteActualizado.nombre=nombre
            #agregar los otros campos del paciente
            pacienteActualizado.genero=genero
            pacienteActualizado.fecha_nacimiento=fecha_nacimiento
            pacienteActualizado.telefono=telefono
            pacienteActualizado.direccion=direccion
            pacienteActualizado.email=email
            pacienteActualizado.save()                                       
            message= "Paciente Actualizado con exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)

    def post(self,request):
        paciente_new=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            body=json.loads(request.body)
            #parametros Paciente
            cedula=body["cedula"]
            nombre = body["nombre"]
            genero = body["genero"]            
            fecha_nacimiento = body["fechanace"]            
            telefono = body["telefono"]
            direccion = body["direccion"]           
            email = body["email"]
            validadorGeneral.validarNombre(nombre)
            validadorGeneral.validarCedula(cedula)
            validadorGeneral.validarGenero(genero)
            validadorGeneral.validarEmail(email)
            validadorGeneral.validarTelefono(telefono)
            validadorGeneral.validar_fecha(fecha_nacimiento)
            paciente_new=Paciente.objects.filter(cedula=cedula)
            #valida que no exista
            print(paciente_new)
            if paciente_new.exists():
                raise Exception ("El paciente ya existe")           
            dd, mm, yyy = fecha_nacimiento.split('/')
            fecha_nacimiento = f"{yyy}-{mm}-{dd}"
            paciente_new = Paciente(nombre=nombre,cedula=cedula,fecha_nacimiento=fecha_nacimiento, genero=genero, direccion=direccion, email=email, telefono=telefono)
            paciente_new.save()
            historiaClinica={"_id":paciente_new.cedula,"historias":{}}
            collection.insert_one(historiaClinica)
            message= "Paciente Grabado con exito\n"
            try:
                nombreContacto = body["nombreContacto"]
                relacion = body["relacion"]
                telefonocontacto = body["telefonocontacto"]
                validadorGeneral.validarNombre(nombreContacto)
                controlPacientes.validarParentesco(relacion)
                validadorGeneral.validarTelefono(telefonocontacto) 
                contacto = informaContacto(paciente = paciente_new,nombre = nombreContacto,relacion = relacion,telefono = telefonocontacto)
                contacto.save()    
                message+="El contacto se registro correctamente\n"
            except Exception as error:
                print("Error al registrar el contacto paciente:\n"+str(error))
                raise Exception("Error al registrar el contacto paciente:\n"+str(error)) 

            if ("idSeguro" in body and "nombreAseguradora" in body and "vigencia"in body) in body:
                try:
                    idSeguro = body["idSeguro"]
                    nombreAseguradora = body["nombreAseguradora"]
                    FechaVigencia = body["vigencia"]
                    #estado = body["estado"]
                    validadorGeneral.validarNombre(nombreAseguradora)
                    controlSeguros.validarPoliza(idSeguro)
                    validadorGeneral.validar_fecha(FechaVigencia)
                    #validadorGeneral.validarEstado(estado)
                    dd, mm, yyy = FechaVigencia.split('/')
                    FechaVigencia = f"{yyy}-{mm}-{dd}"
                    
                    seguro_new = SeguroPaciente.objects.filter(idSeguro=idSeguro)
                    if seguro_new.exists():
                        raise Exception("Ya Existe un Seguro con este ID")
                    seguro_new = SeguroPaciente(idSeguro = idSeguro,nombreAseguradora = nombreAseguradora,paciente = paciente_new,vigencia = FechaVigencia,estado = 1)
                    seguro_new.save()    
                    message=+" El Seguro se registro correctamente \n"
                except Exception as error:
                    print("Error al registrar el Seguro paciente:\n"+str(error))
                    raise Exception("Error al registrar el contacto paciente:\n"+str(error)) 

            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)   
    
    def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])   
            paciente = Paciente.objects.get(cedula=id)
            paciente.estado = 0
            paciente.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status)

class ContactoPaciente(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    #def get(self,request,id=None,cc=None):
    def get(self,request,id=None):        
        contactoPacientes = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])
            print("id ", id)
            if id:
                contactoPacientes = list(informaContacto.objects.filter(paciente_id=id).values())
                
            #if cc:
            #    paciente = Paciente.objects.get(cedula=id)   
            #    print(paciente)            
            #    contactoPacientes = list(Orden.objects.filter(paciente=paciente.cedula).values)
                
            else:
                contactoPacientes = list(informaContacto.objects.values()) 
            if len(contactoPacientes)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Contactos": contactoPacientes}
        return JsonResponse(response,status=status)

    def put(self,request,id=None):
        contactoActualizado=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            
            #actualizar datos
            contactoActualizado = informaContacto.objects.get(paciente_id=id)
            body=json.loads(request.body)
            nombre = body["nombre"]
            relacion = body["relacion"]          
            telefono = body["telefono"]
            validadorGeneral.validarNombre(nombre)
            controlPacientes.validarParentesco(relacion)
            validadorGeneral.validarTelefono(telefono) 
            contactoActualizado.nombre=nombre
            contactoActualizado.relacion = relacion
            contactoActualizado.telefono = telefono
            contactoActualizado.save()                                       
            message= "Contacto Paciente Actualizado con exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])
            body = json.loads(request.body)
            print(body)
            cedulaPaciente = body["paciente"]
            nombre = body["nombre"]
            relacion = body["relacion"]
            telefono = body["telefono"]
            validadorGeneral.validarNombre(nombre)
            controlPacientes.validarParentesco(relacion)
            validadorGeneral.validarTelefono(telefono) 
            paciente = Paciente.objects.get(cedula = cedulaPaciente)
            contacto = informaContacto(paciente_id = paciente.cedula,nombre = nombre,relacion = relacion,telefono = telefono)
            contacto.save()    
            message=" El contacto se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status) 

class Seguro(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        seguroPacientes = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])
            if id:
                seguroPacientes = list(SeguroPaciente.objects.filter(idSeguro=id).values())
            else:
                seguroPacientes = list(SeguroPaciente.objects.values())
                
            if len(seguroPacientes)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Pacientes": seguroPacientes}
        return JsonResponse(response,status=status)
    def put(self,request,id=None):
        seguroActualizado=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["ADM"])
            
            #actualizar datos
            seguroActualizado = SeguroPaciente.objects.get(idSeguro=id)
            #if pacienteActualizado.exists():
            body = json.loads(request.body)
            cedulaPaciente = body["paciente"]
            idSeguro = body["idSeguro"]
            nombreAseguradora = body["nombreAseguradora"]
            FechaVigencia = body["vigencia"]
            validadorGeneral.validarCedula(cedulaPaciente)
            validadorGeneral.validarNombre(nombreAseguradora)
            controlSeguros.validarPoliza(idSeguro)
            validadorGeneral.validar_fecha(FechaVigencia)
            dd, mm, yyy = FechaVigencia.split('/')
            FechaVigencia = f"{yyy}-{mm}-{dd}"
            paciente = Paciente.objects.get(cedula = cedulaPaciente)

            seguro_actualizado = SeguroPaciente.objects.filter(idSeguro=idSeguro)
            if seguro_actualizado.exists():
                raise Exception("Ya Existe un Seguro con este ID")
            seguroActualizado.idSeguro = idSeguro
            seguroActualizado.nombreAseguradora=nombreAseguradora
            seguroActualizado.vigencia = FechaVigencia
            seguroActualizado.paciente = paciente
            seguroActualizado.save()                                       
            message= "Seguro Actualizado con exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])

            body = json.loads(request.body)
            cedulaPaciente = body["paciente"]
            idSeguro = body["idSeguro"]
            nombreAseguradora = body["nombreAseguradora"]
            FechaVigencia = body["vigencia"]

            #estado = body["estado"]
            validadorGeneral.validarCedula(cedulaPaciente)
            validadorGeneral.validarNombre(nombreAseguradora)
            controlSeguros.validarPoliza(idSeguro)
            validadorGeneral.validar_fecha(FechaVigencia)           
            #validadorGeneral.validarEstado(estado)
            dd, mm, yyy = FechaVigencia.split('/')
            FechaVigencia = f"{yyy}-{mm}-{dd}"
            paciente = Paciente.objects.get(cedula = cedulaPaciente)
            seguro_new = SeguroPaciente.objects.filter(idSeguro=idSeguro)
            if seguro_new.exists():
                raise Exception("Ya Existe un Seguro con este ID")
            seguro_new = SeguroPaciente(idSeguro = idSeguro,nombreAseguradora = nombreAseguradora,paciente = paciente,vigencia = FechaVigencia,estado = 1)
            seguro_new.save()    
            message=" El Seguro se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status) 
    
    def delete(self,request,id):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ADM"])   

            seguroEliminado = SeguroPaciente.objects.get(idSeguro=id)
            seguroEliminado.estado = 0
            seguroEliminado.save()
            message = "usuario Eliminado"
            status=200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message} 
        return JsonResponse(response,status=status)

class ModuloMedicamento(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        medicamentos = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ADM","ENF"])

            if id:
                medicamentos = list(Medicamento.objects.filter(idMedicamento=id).values())
            else:
                medicamentos = list(Medicamento.objects.values())
                
            if len(medicamentos)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Medicamentos": medicamentos}
        return JsonResponse(response,status=status)
    
    def put(self,request,id=None):
        medicamentoActualizado=""
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["MED","ADM","ENF"])
            
            body = json.loads(request.body)
            nombre = body["nombre"]
            dosis = body["dosis"]
            presentacion = body["presentacion"]
            precio = body["precio"]
            tiempoTratamiento = body["tiempoTratamiento"]
            validadorGeneral.validarNombre(nombre)
            validadorMedicos.Dosis(dosis)
            validadorMedicos.PresentacionMedicamento(presentacion)
            validadorMedicos.precioMedicamento(precio)

            medicamento_actualizado = Medicamento.objects.filter(idMedicamento=id)
            if not medicamento_actualizado.exists():
                raise Exception("No existe un medicamento con ese ID")
            
            medicamentoActualizado = Medicamento.objects.get(idMedicamento=id)
            medicamentoActualizado.nombre = nombre
            medicamentoActualizado.dosis=dosis
            medicamentoActualizado.presentacion = presentacion
            medicamentoActualizado.precio = precio
            medicamentoActualizado.tiempoTratamiento = tiempoTratamiento
            medicamentoActualizado.save()                                       
            message= "Medicamento Actualizado con exito"
            status= 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message}
        return JsonResponse(response,status=status)
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ADM","ENF"])
            body = json.loads(request.body)
            nombre = body["nombre"]
            #dosis = body["dosis"]
            presentacion = body["presentacion"]
            precio = body["precio"]
            #tiempoTratamiento = body["tiempoTratamiento"]
            validadorGeneral.validarNombre(nombre)
            #validadorMedicos.Dosis(dosis)
            #validadorMedicos.PresentacionMedicamento(presentacion)
            #validadorMedicos.precioMedicamento(precio)

            #seguro_new = SeguroPaciente.objects.filter(idSeguro=idSeguro)
            #if seguro_new.exists():
            #    raise Exception("Ya Existe un Seguro con este ID")
            medicamento = Medicamento(nombre = nombre,presentacion  = presentacion,precio = precio)
            medicamento.save()    
            message=" El Medicamento se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def delete(self,request):
        pass

class ModuloOrdenMedicamento(View):
    #def get(self,request,id=None, cc=None):
    def get(self,request,cc=None):
        ordenMedicamento = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])
            #if id:
            #    print ("ingreso al id")
                #ordenMedicamento = OrdenMedicamento.objects.get(id=id)
            #    ordenMedicamento = list(OrdenMedicamento.objects.filter(id=id).values())
            if cc:
                paciente = Paciente.objects.get(cedula=cc)   
                print(paciente)            
                ordenePaciente = Orden.objects.get(cedulaPaciente=paciente.cedula,estado=1)
                print(ordenePaciente)

                ordenMedicamento = list(OrdenMedicamento.objects.filter(idOrden=ordenePaciente).values())

                print(ordenMedicamento)
                for oMedicamento in ordenMedicamento:
                    medicamento=Medicamento.objects.get(idMedicamento=oMedicamento["idMedicamento_id"])
                    oMedicamento["nombre"]=medicamento.nombre
                print(ordenMedicamento)
            else:
                ordenMedicamento = list(OrdenMedicamento.objects.values())
                
            if len(ordenMedicamento)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "OrdenesMedicamentos": ordenMedicamento}
        return JsonResponse(response,status=status)
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])
            body = json.loads(request.body)
            idOrden = body["idOrden"]
            item = body["item"]
            IdMedicamento = body["IdMedicamento"]
            dosis = body["dosis"]
            tiempoTratamiento = body["tiempoTratamiento"]
            validadorMedicos.Dosis(dosis)
            #faltan los validadores de los otros campos

            #ordenMedicamento_new = OrdenMedicamento.objects.filter()
            #if seguro_new.exists():
            #    raise Exception("Ya Existe un Seguro con este ID")
            medicamento = Medicamento.objects.get(IdMedicamento=IdMedicamento)
            orden = Orden.objects.get(idOrden=idOrden)

            ordenMedicamento_new = OrdenMedicamento(idOrden = orden,item = item,IdMedicamento = medicamento,dosis = dosis,tiempoTratamiento = tiempoTratamiento)
            ordenMedicamento_new.save()    
            message=" se registro la orden de Medicamento correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class ConsultaMedica(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        pass
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)
            
            cedulaPaciente = body["cedulaPaciente"]
            #cedulaMedico = body["cedulaMedico"]
            #fechaRegistro = body["fechaRegistro"]
            motivoConsulta = body["MotivoConsulta"]
            sintomas = body["Sintomas"]
            diagnostico = body["diagnostico"]
            medico= sesion.usuario
            #medico = PersonalClinica.objects.get(cedula=cedulaMedico)
            paciente = Paciente.objects.get(cedula=cedulaPaciente)
            fechaActual=str(datetime.now())
            fechaRegistro = date.today().strftime('%Y-%m-%d')
           #validaciones
            validadorMedicos.mConsulta(motivoConsulta)
            validadorMedicos.sintomas(sintomas)

            orden = Orden(cedulaPaciente=paciente,cedulaMedico=medico,fechaRegistro=fechaRegistro)
            orden.save()

            historiaActual={"fecha":fechaActual,
                "medico":str(medico.usuario)
                }
            historiaActual["MotivoConsulta"] = motivoConsulta
            historiaActual["Sintomas"] = sintomas
            historiaActual["Diagnostico"] = diagnostico
            historiaActual["idOrden"] = orden.id
            
            if ("medicamentos" in body or "procedimientos"in body) and "ayudasDiagnosticas" in body:
                orden.delete()
                raise Exception ("no se puede ordenar ayudas diagnosticas y medicamentos o procedimientos al tiempo")

            item = 0
            historiaActual["item"]={}
            try:  
                if "medicamentos" in body:
                    medicamentos = body["medicamentos"]
                    
                    for medicamento in medicamentos:
                        #Busco cual fue el ultimo ID de orden registrado
                        #idOrdenAnterior = Orden.objects.aggregate(Max('id'))['id__max']
                        #aumenta 1 para determinar cual es el siguiente ID de orden que se le va a asignar a esta orden
                        #idOrden = orden.id
                        #item = body["item"]
                        item +=1
                        idMedicamento = medicamento["idMedicamento"]
                        dosis = medicamento["dosis"]
                        tiempoTratamiento = medicamento["tiempoTratamiento"]
                        validadorMedicos.Dosis(dosis)
                        validadorMedicos.Tmedicamento(tiempoTratamiento)

                        #busca el medicamento con el id si no lo encuentra revienta 
                        medicamento = Medicamento.objects.get(idMedicamento=idMedicamento)
                        medicamentoHistoria={
                            "item": item,
                            "medicamento": medicamento.nombre,
                            "dosis": dosis,
                            "tiempoTratamiento":tiempoTratamiento                            
                        }
                        ordenMedicamento_new = OrdenMedicamento(idOrden = orden,item = item,idMedicamento = medicamento,dosis = dosis,tiempoTratamiento = tiempoTratamiento)
                        ordenMedicamento_new.save()  
                        historiaActual["item"][str(item)]=medicamentoHistoria
                        print("Se registro la OrdenMedicamento")  
            except Exception as error:
                orden.delete()
                print("Error en el primer try de Medicamento"+str(error))
                raise Exception(str(error))          
            
            try:
                if "procedimientos" in body:
                    procedimientos = body["procedimientos"]
                    for procedimiento in procedimientos:
                        #Busco cual fue el ultimo ID de orden registrado
                        #idOrdenAnterior = Orden.objects.aggregate(Max('id'))['id__max']
                        #aumenta 1 para determinar cual es el siguiente ID de orden que se le va a asignar a esta orden
                        #idOrden = orden.id
                        item +=1
                        idProcedimiento = procedimiento["idProcedimiento"]
                        cantidad = procedimiento["cantidad"]
                        asistenciaEspecializada = procedimiento["asistenciaEspecializada"]
                        validadorMedicos.Cantidad(cantidad)
                        procedimiento = Procedimiento.objects.get(codProcedimiento=idProcedimiento)
                        procedimientoHistoria={
                            "item": item,
                            "procedimiento": procedimiento.nombreProcedimiento,
                            "cantidad": cantidad,
                            "asistenciaEspecializada": asistenciaEspecializada                          
                        }
                        #revienta si no existe el procedimiento
                        ordenProcedimiento = OrdenProcedimiento(idOrden=orden,cantidad=cantidad,item= item,idProcedimiento=procedimiento,asistenciaEspecializada=asistenciaEspecializada)
                        ordenProcedimiento.save()
                        historiaActual["item"][str(item)]=procedimientoHistoria
            except Exception as error:
                print("Error en el primer try de procedimiento"+str(error))
                orden.delete()
                raise Exception(str(error))
            
            try:
                if "ayudasDiagnosticas" in body:
                    ayudaDiagnosticas = body["ayudasDiagnosticas"]
                    for ayuda in ayudaDiagnosticas:
                        item +=1
                        idAyuda = ayuda["ayuda"]
                        asistenciaEspecializada = ayuda["requiereEspecialista"]
                        cantidad = ayuda["cantidad"]
                        validadorMedicos.Cantidad(cantidad)
                        ayuda = Ayuda.objects.get(codAyuda=idAyuda)
                        ayudaHistoria={
                            "item": item,
                            "procedimiento": ayuda.nombreAyuda,
                            "cantidad": cantidad,
                            "asistenciaEspecializada": asistenciaEspecializada                          
                        }
                        ordenAyuda = OrdenAyudaDiagnostica(idOrden=orden,item= item,cantidad=cantidad,idAyuda=ayuda,asistenciaEspecializada=asistenciaEspecializada)
                        ordenAyuda.save()
                        historiaActual["item"][str(item)]=ayudaHistoria
            except Exception as error:
                print("Error en el primer try de AyudaDiagnostica"+str(error))
                orden.delete()
                raise Exception(str(error))
            
            #try:
            #    if "ayudaDiagnosticas" in body:
            #        print("entra")
            #        nombreAyuda = body["ayudaDiagnosticas"]["nombreAyuda"]
            #        cantidad = body["ayudaDiagnosticas"]["cantidad"]
            #        asistenciaEspecializada = body["ayudaDiagnosticas"]["asistenciaEspecializada"]
            #        ordenAyuda = OrdenAyudaDiagnostica(idOrden= orden,nombreAyuda=nombreAyuda,cantidad=cantidad,asistenciaEspecializada=asistenciaEspecializada)
            #        ordenAyuda.save()
            #        print("creada orden con id " +str(ordenAyuda.id))
            #except Exception as error:
            #    print("Error en el primer try de ayudaDiagnostica"+str(error))
            #    orden.delete()
            #    raise Exception(str(error))            

            #historia=collection.find_one({'_id': paciente.cedula})
            historia=collection.find_one({'_id': str(paciente.cedula)})
            historia["historias"][fechaActual]=historiaActual 
            collection.update_one({'_id': str(paciente.cedula)}, {'$set': historia})

            message="se agrego registro a historia clinica"
            message=" La historia de creo correctamente "
            status = 200        
        except Exception as error:
            #rden.delete()
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class ModuloVisitaEnfermera(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        visitasEnfermeras = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ENF"])
            if id:
                visitasEnfermeras = list(VisitaEnfermera.objects.filter(idVisita=id).values())
            else:
                visitasEnfermeras = list(VisitaEnfermera.objects.values())
                
            if len(visitasEnfermeras)>0:
                message = "registros encontrados"
            else:
                message="registros de Vistas no encontrados"
                status = 400
                raise Exception("Registros de visitas Enfermeras no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Visitas": visitasEnfermeras}
        return JsonResponse(response,status=status)
        
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["ENF","MED"])
            body = json.loads(request.body)
            presionArterial = body["presionArterial"]
            temperatura = body["temperatura"]
            pulso = body["pulso"]
            nivelOxigeno = body["nivelOxigeno"]
            cedulaPaciente = body["cedulaPaciente"]
            usuarioEnfermera = sesion.usuario
            observaciones = body["observaciones"]
            recordatorioSiguienteVisia = body["recordatorioSiguienteVisia"]
            
            #fechaActual=str(datetime.now())
            fechaRegistro = date.today().strftime('%Y-%m-%d')

            paciente = Paciente.objects.get(cedula=cedulaPaciente)
            
            validadorEnfermeras.validarPresionArterial(presionArterial)
            validadorEnfermeras.validarTemperatura(temperatura)
            validadorEnfermeras.validarPulso(pulso)
            validadorEnfermeras.validarNivelOxigeno(nivelOxigeno)
            orden=None
            if "idOrden_id" in body :
                idOrden = body["idOrden_id"]

                try:                    
                    orden = Orden.objects.get(id=idOrden)
                except Exception as error:
                    print("Error al Buscar la Orden en el registro de la visita :\n"+str(error))
                    raise Exception("Error al Buscar la Orden en el registro de la visita:\n"+str(error)) 
                
                if paciente.cedula != orden.cedulaPaciente.cedula:
                    raise Exception("La orden no pertenece a este paciente")
                
                if orden.estado == 0:
                    raise Exception("La Orden ya fue atendida.")                

                ordenAyuda = OrdenAyudaDiagnostica.objects.filter(idOrden=orden)
                if ordenAyuda.exists():
                    raise Exception("Las enfermeras no pueden realizar Ayudas Diagnosticas")

                #visita_New = VisitaEnfermera(fecha=fechaRegistro,presionArterial=presionArterial,temperatura=temperatura,pulso=pulso,nivelOxigeno=nivelOxigeno,cedulaPaciente=paciente,usuarioEnfermera=usuarioEnfermera,idOrden=orden,observaciones=observaciones,recordatorioSiguienteVisia=recordatorioSiguienteVisia) 
                #visita_New.save()   
                


            visita_New = VisitaEnfermera(fecha=fechaRegistro,presionArterial=presionArterial,temperatura=temperatura,pulso=pulso,nivelOxigeno=nivelOxigeno,cedulaPaciente=paciente,usuarioEnfermera=usuarioEnfermera,idOrden=orden,observaciones=observaciones,recordatorioSiguienteVisia=recordatorioSiguienteVisia) 
            visita_New.save()

            message = "Se registro la visita correctamente"
            status=200    

        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class ModuloProcedimiento(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        procedimientos = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])

            if id:
                procedimientos = list(Procedimiento.objects.filter(codProcedimiento=id).values())
            else:
                procedimientos = list(Procedimiento.objects.values())
                
            if len(procedimientos)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Procedimientos": procedimientos}
        return JsonResponse(response,status=status)
    
    def put(self,request,id=None):
        pass
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)

            nombreProcedimiento = body["nombreProcedimiento"]
            precio = body["precio"]
            validadorGeneral.validarNombre(nombreProcedimiento)

            procedimiento = Procedimiento(nombreProcedimiento = nombreProcedimiento,precio  = precio)
            procedimiento.save()    
            message=" El Procedimiento se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def delete(self,request):
        pass

class ModuloOrdenProcedimiento(View):

    def get(self,request,id=None,cc=None):
        ordenProcedimiento = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])

            if id:
                #ordenMedicamento = OrdenMedicamento.objects.get(id=id)
                ordenProcedimiento = list(OrdenProcedimiento.objects.filter(id=id).values())
            elif cc:
                paciente = Paciente.objects.get(cedula=cc)            
                ordenePaciente = Orden.objects.get(cedulaPaciente=paciente.cedula,estado=1)
                ordenProcedimiento = list(OrdenProcedimiento.objects.filter(idOrden=ordenePaciente).values())
                for oProcedimiento in ordenProcedimiento:
                    nombreProcedimiento=Procedimiento.objects.get(codProcedimiento=oProcedimiento["idProcedimiento_id"])
                    oProcedimiento["nombre"]=nombreProcedimiento.nombreProcedimiento
                print(ordenProcedimiento)

            else:
                ordenProcedimiento = list(OrdenProcedimiento.objects.values())
                
            if len(ordenProcedimiento)>0:
                message = "registros encontrados"
            else:
                message="registros no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
            print(str(error))
        response = {"message":message, "OrdenesProcedimientos": ordenProcedimiento}
        return JsonResponse(response,status=status)
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)
            idOrden = body["idOrden"]
            item = body["item"]
            codProcedimiento = body["codProcedimiento"]
            asistenciaEspecializada = body["asistenciaEspecializada"]
            #faltan los validadores de los otros campos

            #ordenMedicamento_new = OrdenMedicamento.objects.filter()
            #if seguro_new.exists():
            #    raise Exception("Ya Existe un Seguro con este ID")
            procedimiento = Procedimiento.objects.get(codProcedimiento=codProcedimiento)
            orden = Orden.objects.get(idOrden=idOrden)

            ordenProcedimiento_new = OrdenProcedimiento(idOrden = orden,item = item,idProcedimiento = procedimiento,asistenciaEspecializada = asistenciaEspecializada)
            ordenProcedimiento_new.save()    
            message=" se registro la orden de Procedimiento correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class ModuloAyuda(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=None):
        ayudas = None
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED","ENF"])

            if id:
                ayudas = list(Ayuda.objects.filter(codAyuda=id).values())
            else:
                ayudas = list(Ayuda.objects.values())
                
            if len(ayudas)>0:
                message = "Ayudas encontrados"
            else:
                message="Ayudas no encontrados"
                status = 400
                raise Exception("Registros no encontrados")
            status=200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message":message, "Ayudas": ayudas}
        return JsonResponse(response,status=status)
    
    def put(self,request,id=None):
        pass
        
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)

            nombreProcedimiento = body["nombreProcedimiento"]
            precio = body["precio"]
            validadorGeneral.validarNombre(nombreProcedimiento)

            procedimiento = Procedimiento(nombreProcedimiento = nombreProcedimiento,precio  = precio)
            procedimiento.save()    
            message=" El Procedimiento se registro correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

    def delete(self,request):
        pass
class ModuloOrdenAyudaDiagnostica(View):
    def get(self,request):
        pass
    def put(self,request):
        pass
    def post(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion = Sesion.objects.get(token = token)
            validarRol(sesion,["MED"])
            body = json.loads(request.body)
            idOrden = body["idOrden"]
            nombreAyuda = body["nombreAyuda"]
            cantidad = body["cantidad"]
            asistenciaEspecializada = body["asistenciaEspecializada"]
    
            orden = Orden.objects.get(idOrden=idOrden)

            ordenAyuda_new = OrdenAyudaDiagnostica(idOrden=orden,nombreAyuda=nombreAyuda,cantidad=cantidad,asistenciaEspecializada=asistenciaEspecializada)
            ordenAyuda_new.save()
            message=" se registro la orden de Procedimiento correctamente "
            status = 200        
        except Exception as error:
            message=str(error)
            status=400
        response ={"message": message}
        return JsonResponse(response,status=status)

class Factura(View):
    def get(self,request):
        pass
    def put(self,request):
        pass
    def post(self,request):
        pass

