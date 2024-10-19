def validarDatosUsuario (rol1,usuario,password):
    rol=rol1.upper()
    if rol == "" or rol == None:
        print("Rol no puede ser nulo")
        raise Exception("Rol no valido")
    if  rol != "RH" and rol != "ADM" and rol != "MED" and rol != "ENF":
        print("Rol no valido, entre RH - ADM - MED - ENF")
        raise Exception("Rol no valido, entre RH - ADM - MED - ENF") 

    if usuario == None or usuario == "":
        print("usuario no valido")
        raise Exception("usuario no valido")
    
    #Validar contraseña
    if password == None or password == "":
        print("Contraseña no valida")
        raise Exception("contraseña no valida")


def validarPersonaUnica (clinica,nuevo):
    for personalClinica in clinica.empleadosClinica:
        if(personalClinica.usuario == nuevo.usuario or personalClinica.usuario != None) and personalClinica.cedula == nuevo.cedula:
            raise Exception("Usuario ya registrado")
   

def buscarPersona(clinica,cedula):
    for personalClinica in clinica.empleadosClinica:
        if personalClinica.cedula==cedula:
            return personalClinica
    print ("persona no encontrada")
    raise Exception ("persona no encontrada")


def buscarPersonaPorUsuario (clinica,usuario):
    for personalClinica in  clinica.empleadosClinica:
        if personalClinica.usuario == usuario:
            return personalClinica
    raise Exception("no se encontro persona con el usuario ")

def ActualizarPersonal (clinica,persona):
    for i in range(len(clinica.empleadosClinica)):
        if clinica.empleadosClinica[i].cedula == persona.cedula:
            clinica.empleadosClinica[i] = persona
            print("Registro actualizado")
            print(clinica.empleadosClinica[i])
            return
    raise Exception("Error al actualizar")
    
""" 
def ActualizarPersonal (clinica,persona):
    for index, persona.cedula in enumerate(clinica.empleadosClinica.cedula):
        if persona.cedula == clinica.empleadosClinica.cedula:
            clinica.empleadosClinica[index] = persona
            print("Registro actualizado")
            print(clinica.empleadosClinica[index])
            return

    raise Exception("Error al actualizar") """