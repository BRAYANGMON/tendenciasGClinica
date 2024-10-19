def ImprimirAsistencia(clinica,cedula):
    for i in range(len(clinica.asistencias)):
        if clinica.asistencias[i].cedula == cedula:
            print("--------------\n")
            print(clinica.asistencias[i])
        return   
    raise Exception("Error al buscar asistencia")
#validar con andres

def VerificarAsistencia(clinica, cedula, fecha):
    for asistencia in clinica.asistencias:
        if asistencia.cedula == cedula and asistencia.fechaRegistro == fecha:
            print("Empleado ya registro asistencia")
            return True
    print("")
    print("se registro asistencia")
    return False

