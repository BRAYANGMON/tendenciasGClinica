from datetime import datetime

def buscarFacturaPaciente(clinica, cedula_paciente): 
    copagoAno=0
    for factura in clinica.facturas:
        if factura.paciente == cedula_paciente  and (datetime.datetime.now().year == factura.fecha.year):
                copagoAno=copagoAno + factura.copago
#    raise Exception ("Factura no encontrada")
    return copagoAno

def buscarUltimaHistoria(clinica, cedulaP, fecha):
     for historiaPaciente in clinica.historiaClinica:
          if historiaPaciente['fecha']== fecha and historiaPaciente['cedula']==cedulaP:
               return historiaPaciente
          

