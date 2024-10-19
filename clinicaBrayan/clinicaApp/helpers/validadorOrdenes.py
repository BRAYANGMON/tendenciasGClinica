def validarNombreOrden (nombre):
    if nombre == "" or nombre == None:
        print("nombre de la Orden no valido")
        raise Exception("nombre de la orden no valido")
    

def asistenciaEspecializada (asistenciaEspecializada):
    if asistenciaEspecializada == "" or asistenciaEspecializada == None:
        print("nombre Asistencia Especializda no valido")
        raise Exception("nombre Asistencia Especializda no valido")
    
def validarID (idOrden):
   ## if cedula.isdigit() and len(cedula) != 10 : Preguntar
    if idOrden == "" or idOrden == None:
        print ("el ID de la orden no puede estar vacio")
        raise Exception("el ID de la orden no puede estar vacio")
    try:
        idOrden = int(idOrden)
    except:
        raise Exception("el ID de la orden debe ser numerica")
    