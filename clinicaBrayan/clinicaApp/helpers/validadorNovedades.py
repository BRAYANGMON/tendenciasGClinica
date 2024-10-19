import re

def TipoNovedad (tipo):
    if tipo == "" or tipo == None:
        print("tipo de novedad no valido")
        raise Exception("tipo de novedad no valido")

def ValidarTiempo (dias):
    if dias == "" or dias == None:
        print("Tiempor de la novedad no valido ")
    try:
        dias = int(dias)
    except:
        raise Exception("no ingreso los dias de la novedad en el formato correcto")
    
