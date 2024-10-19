#motivo de la consulta 
#sintomas
def mConsulta (motivo):
    if motivo == "" or motivo == None:
        print("el motivo de la consulta no pude quedar vacio")
        raise Exception("el motivo de la consulta no pude quedar vacio")
    
def sintomas (sintomas):
    if sintomas == "" or sintomas == None:
        print("El campo de los Sintomas no puede quedar vacio")
        raise Exception("el motivo de la consulta no pude qyedar vacio")
    
def Medicamento (nombre):
    if nombre ==""or nombre==None :
        print ("El campo nombre de medicamento no puede ser vacio")
        raise Exception("El campo nombre de medicamento no puede ser vacio")

def Tmedicamento (tiempo):
    if tiempo ==""or tiempo==None :
        print ("Tiempo del medicamento no puede ser vacio")
        raise Exception("Tiempo del medicamento no puede ser vacio")

def Dosis (dosis):
    if dosis ==""or dosis==None :
        print ("El campo Dosis no puede ser vacio")
        raise Exception("El campo Dosis no puede ser vacio")

# Validaciones de las ayudas diagnosticas 
def NombreAyuda (nombreAyuda):
    if nombreAyuda == "" or nombreAyuda == None:
        print("El Campo nombre de ayuda Diagnostica no puede estar vacio")
        raise Exception("El Campo nombre de ayuda Diagnostica no puede estar vacio")
 
def CantidadAyuda (cantidad):
   ## if cedula.isdigit() and len(cedula) != 10 : Preguntar
    if cantidad == "" or cantidad == None:
        print ("cantidad de ayuda diagnostica no valida")
        raise Exception("cantidad de ayuda diagnostica no valida")
    try:
        cantidad = int(cantidad)
    except:
        raise Exception("la cantidad de ayuda diagnostica debe ser numerica")

# Validaciones de las Procedimientos
def NombreProcedimiento (nombreProc):
    if nombreProc == "" or nombreProc == None:
        print("El Campo nombre de procedimiento no puede estar vacio")
        raise Exception("El Campo nombre de procedimiento no puede estar vacio")
 

def RepeticionesProc (cantidad):
    if cantidad == "" or cantidad == None:
        print ("cantidad de veces del procedimiento no valida")
        raise Exception("cantidad de veces del procedimiento no valida")
    try:
        cantidad = int(cantidad)
    except:
        raise Exception("la cantidad de veces del procedimiento debe ser numerica")
    
def FrecuenciaProcedimiento (frecuenciaProc):
    if frecuenciaProc == "" or frecuenciaProc == None:
        print("El Campo frecuencia de procedimiento no puede estar vacio")
        raise Exception("El Campo frecuencia de procedimiento no puede estar vacio")
    

def Cantidad (cantidad):
   ## if cedula.isdigit() and len(cedula) != 10 : Preguntar
    if cantidad == "" or cantidad == None or cantidad == "e":
        print ("cantidad  no valida")
        raise Exception("cantidad a no valida")
    try:
        cantidad = int(cantidad)
    except:
        raise Exception("la cantidad debe ser numerica")
 