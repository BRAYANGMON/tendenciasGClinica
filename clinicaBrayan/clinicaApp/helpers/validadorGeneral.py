import re

def validarNombre (nombre):
    if nombre == "" or nombre == None:
        print("nombre no valido")
        raise Exception("nombre no valido")
    
def validarCedula (cedula):
   ## if cedula.isdigit() and len(cedula) != 10 : Preguntar
    if cedula == "" or cedula == None or len(cedula) >10:
        print ("Cedula no valida")
        raise Exception("cedula no valida: por favor valide si el campo lo envio sin el digito o supero los 10 digitos")
    try:
        cedula = int(cedula)
    except:
        raise Exception("la cedula debe ser numerica")
    
# Preguntar
def validarEmail(email):
    if email==None or email=="":
        print("Email no valido")
        raise Exception("Email no valido")
    try:
        expresion_regular = '^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$'
        if not re.match(expresion_regular,email.lower()): 
            print("Correo no valido ")
            raise Exception("Correo no valido ")

    except:
        raise Exception("Correo no valido ")

#Preguntar
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

 # numero de telefono 
def validarTelefono (telefono):
   ## if cedula.isdigit() and len(telefono) != 10 : Preguntar
    if telefono == "" or telefono == None or len(telefono) !=10:
        print ("telefono no valido")
        print(len(telefono))
        raise Exception("telefono no valida")
    try:
        telefono = int(telefono)
    except:
        raise Exception("el telefono debe ser numerica")
    
def validarFechaNacimiento (fecha):
    if fecha == "" or fecha == None:
        print("fecha no valido")
        raise Exception("fecha no valido")
    
def validar_fecha(fecha):
    if fecha == "" or fecha == None:
        print("la fecha es obligatoria")
        raise Exception("No se ingreso la fecha")
    try:
        #Fecha Formato DD/MM/AAA
        expresion_regular = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        if not re.match(expresion_regular, fecha):
            print("Formato Fecha no valido")
            raise Exception("Formato Fecha no valido")
    except:
        raise Exception("Fecha ingresada no esta en el formato adecuado")
   
def validarDireccion (direccion):
    if direccion == "" or direccion == None:
        print("direccion no valido")
        raise Exception("direccion no valido")

def validarGenero (genero):
    if genero == "" or genero == None:
        print("genero no valido")
        raise Exception("genero no valido")
    if genero !="h" and genero !="H" and genero !="m" and genero !="M":
        print("genero incorrecto")
        raise Exception("Genero incorrecto") 


def ValidarPassword (passw):
    if len(passw) <8:
        print ("Contraseña no puede tener menos de 8 Caracteres ")
        print(len(passw))
        raise Exception("Contraseña no puede tener menos de 8 Caracteres ")
    try:
        expresion_regular = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$'
        if not re.match(expresion_regular,passw): 
            print("Contraseña No cumple con los requisitos de seguridad ")
            print("Debe incluir una mayúscula, un número, un carácter especial y contener por lo menos 8 caracteres")
            raise Exception("Contraseña No cumpl con los requisitos de seguridad ")
    except:
        raise Exception("Contraseña No cumple con los requisitos de seguridad  ")
    