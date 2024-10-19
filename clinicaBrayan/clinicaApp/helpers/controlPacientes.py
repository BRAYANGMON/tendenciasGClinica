def buscarPaciente(clinica,cedula):
    for pacienteClinica in clinica.pacientes:
        if pacienteClinica.cedula==cedula:
            return pacienteClinica
    print ("paciente no encontrado")
    raise Exception ("paciente no encontrado")

def ActualizarPaciente (clinica,paciente):
    for i in range(len(clinica.pacientes)):
        if clinica.pacientes[i].cedula == paciente.cedula:
            clinica.pacientes[i] = paciente
            print("Registro Paciente actualizado")
            print("")
            print(clinica.pacientes[i])
            return

    raise Exception("Error al actualizar Paciente")

#def validarPacienteUnico (clinica,nuevo):
def validarPacienteUnico (clinica,nuevo):
    for pacienteClinica in clinica.pacientes:
        if(pacienteClinica.cedula == nuevo.cedula):
            raise Exception("Paciente ya registrado")
    print("")   
        
def validarParentesco (pariente):
    if pariente == "" or pariente == None:
        print("parentesco no valido")
        raise Exception("parentesco no valido")