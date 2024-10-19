def buscarOrdenMedicamento(clinica,idOMedicamento):
    for ordenMedicamento in clinica.ordenesMedicamentos:
        if ordenMedicamento.idOrden==idOMedicamento:
            return ordenMedicamento    
    #print ("Orden Medicamento no encontrada")
    raise Exception ("Orden Medicamento no encontrada")

def buscarOrdenMedicamentoPaciente(clinica,idOMedicamento,cedula):
    for ordenMedicamento in clinica.ordenesMedicamentos:
        if ordenMedicamento.idOrden==idOMedicamento and ordenMedicamento.cedulaPaciente == cedula:
            return ordenMedicamento
    #print ("La orden no pertenece a ese paciente")
    raise Exception ("La orden de medicamento no pertenece al paciente")

def buscarOrdenProcedimientoPaciente(clinica,idOProcedimiento,cedula):
    for ordenProcedimiento in clinica.ordenesProcedimientos:
        if ordenProcedimiento.idOrden==idOProcedimiento and ordenProcedimiento.cedulaPaciente == cedula:
            return ordenProcedimiento
    #print ("La orden no pertenece a ese paciente")
    raise Exception ("La orden del procedimiento no pertenece al paciente")

def buscarOrdenProcedimientos(clinica,idOProcedimiento):
    for ordenProcedimiento in clinica.ordenesProcedimientos:
        if ordenProcedimiento.idOrden==idOProcedimiento:
            return ordenProcedimiento
    print ("Orden Procedimiento no encontrada")
    raise Exception ("Orden Procedimiento no encontrada")




def ordenencontrada(clinica,idOMedicamento):
    for i in range(len(clinica.ordenesMedicamentos)): 
        if clinica.ordenesMedicamentos[i].idOrden==idOMedicamento:
            return True
    print ("Orden Medicamento no encontrada")
    raise Exception ("Orden Medicamento no encontrada") 

