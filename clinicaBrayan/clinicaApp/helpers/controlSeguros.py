def validarPoliza (poliza):
   ## if cedula.isdigit() and len(cedula) != 10 : Preguntar
    if poliza == "" or poliza == None:
        print ("Poliza no valida")
        raise Exception("Poliza no valida")
    try:
        poliza = int(poliza)
    except:
        raise Exception("la cedula debe ser numerica")

def ValidarPolizaUnica(clinica, poliza):
    for polizaPaciente in clinica.seguros:
        print (poliza)
        if polizaPaciente.poliza == poliza:
            raise Exception("Poliza ya registrado")
    print("") 
            
def buscarPoliza(clinica, poliza):
    for polizaClinica in clinica.seguros:
        if polizaClinica.poliza==poliza:
            return polizaClinica
    print ("poliza no encontrado")
    raise Exception ("poliza no encontrado")
