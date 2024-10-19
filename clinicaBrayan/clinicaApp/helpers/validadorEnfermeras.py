def validarPulso (pulso):
    if pulso == "" or pulso == None:
        print("Pulso no valido")
        raise Exception("Pulso no valido")
    
def validarMedicamento (medicamento):
    if medicamento == "" or medicamento == None:
        print("Medicamento no valido")
        raise Exception("Medicamento no valido")
    
def validarPresionArterial (presionArterial):
    if presionArterial == "" or presionArterial == None:
        print ("presion Arterial no valida")
        raise Exception("presion Arterial no valida")
    try:
        presionArterial = float(presionArterial)
    except:
        raise Exception("Formato Presion arterial no valido ")
    
def validarTemperatura (temperatura):
    if temperatura == "" or temperatura == None:
        print ("Temperatura no valida")
        raise Exception("Temperatura no valida")
    try:
        temperatura = float(temperatura)
    except:
        raise Exception("Formato temperatura no valido ")
    
def validarNivelOxigeno (nivelOxigeno):
    if nivelOxigeno == "" or nivelOxigeno == None:
        print ("Nivel Oxigeno no valida")
        raise Exception("Nivel Oxigeno no valida")
    try:
        nivelOxigeno = float(nivelOxigeno)
    except:
        raise Exception("NIvel Oxigeno no valido ")