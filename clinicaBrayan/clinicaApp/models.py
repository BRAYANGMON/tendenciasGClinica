from django.db import models

# Create your models here.
class PersonalClinica(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    cedula = models.BigIntegerField(primary_key=True, null=False, blank=False)
    email = models.CharField(null=False, max_length=30)
    telefono = models.CharField(max_length=10, null=False)
    fecha_nacimiento = models.DateField(null=False)
    direccion = models.CharField(max_length=30)
    rol = models.CharField(max_length=3, null=False, blank=False)
    usuario = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=20)
    estado = models.IntegerField(null=False, blank=False)

class Novedad(models.Model):
    idNovedad = models.AutoField(primary_key=True)
    tipo = models.CharField(null=False, max_length=30)
    cedula = models.ForeignKey(PersonalClinica, null=False, on_delete=models.CASCADE)
    tiempo = models.IntegerField(null=False)
    fechaRegistro = models.DateField(null=False)
    observaciones = models.CharField(max_length=250)

class Paciente(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    cedula = models.BigIntegerField(primary_key=True, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=False)
    genero = models.CharField(max_length=1)
    direccion = models.CharField(max_length=30)
    email = models.CharField(null=False, max_length=30)
    telefono = models.CharField(max_length=10, null=False)
    estado = models.IntegerField(null=False, blank=False, default = 1)

class informaContacto(models.Model):
    idContacto = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, null=False, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=False)
    relacion = models.CharField(null=False, max_length=30)
    telefono = models.CharField(max_length=10, null=False)

class SeguroPaciente(models.Model):
    idSeguro = models.IntegerField(primary_key=True, null=False, blank=False)
    nombreAseguradora = models.CharField(max_length=30, null=False)
    paciente = models.ForeignKey(Paciente, null=False, on_delete=models.CASCADE)
    vigencia = models.DateField(null=False)
    estado = models.IntegerField(null=False, blank=False)

class Asistencia(models.Model):
    idNovedad = models.AutoField(primary_key=True)
    tipo = models.CharField(null=False, max_length=30)
    cedula = models.ForeignKey(PersonalClinica, null=False, on_delete=models.CASCADE)
    fechaRegistro = models.DateField(null=False)

class Medicamento(models.Model):
    idMedicamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    presentacion = models.CharField(max_length=30, null=False)
    precio =  models.FloatField(null=False, blank=False)

class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    cedulaPaciente = models.ForeignKey(Paciente, null=False, on_delete=models.CASCADE)
    cedulaMedico = models.ForeignKey(PersonalClinica, null=False, on_delete=models.CASCADE)
    fechaRegistro = models.DateField(null=False)
    estado = models.IntegerField(null=False, blank=False, default = 1)

class OrdenMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.ForeignKey(Orden, null=False, on_delete=models.CASCADE)
    item = models.IntegerField(null=False, blank=False, default = 0)
    idMedicamento = models.ForeignKey(Medicamento, null=False, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=30, null=False)
    tiempoTratamiento = models.IntegerField(null=False, blank=False, default = 0)
    
class Procedimiento(models.Model):
    codProcedimiento = models.AutoField(primary_key=True)
    nombreProcedimiento = models.CharField(max_length=30, null=False)
    precio = models.FloatField(null=False, blank=False)

class OrdenProcedimiento(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.ForeignKey(Orden, null=False, on_delete=models.CASCADE)
    item = models.IntegerField(null=False, blank=False, default = 0)
    cantidad = models.IntegerField(null=True)
    idProcedimiento = models.ForeignKey(Procedimiento, null=False, on_delete=models.CASCADE)
    asistenciaEspecializada = models.CharField(max_length=30, null=False)

class Ayuda(models.Model):
    codAyuda = models.AutoField(primary_key=True)
    nombreAyuda = models.CharField(max_length=30, null=False)
    precio = models.FloatField(null=False, blank=False)

class OrdenAyudaDiagnostica(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.ForeignKey(Orden, null=False, on_delete=models.CASCADE)
    item = models.IntegerField(null=False, blank=False, default = 0)
    cantidad = models.IntegerField(null=True)
    idAyuda = models.ForeignKey(Ayuda, null=True, on_delete=models.CASCADE)
    asistenciaEspecializada = models.CharField(max_length=30, null=False)
    revision = models.BooleanField(null=False,default=False)

class VisitaEnfermera(models.Model):
    idVisita = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False)
    presionArterial = models.FloatField(null=False, blank=False)
    temperatura = models.FloatField(null=False, blank=False)
    pulso = models.CharField(null=False, blank=False, max_length=10)
    nivelOxigeno = models.FloatField(null=False, blank=False)
    cedulaPaciente = models.ForeignKey(Paciente, null=False, on_delete=models.CASCADE)
    usuarioEnfermera = models.ForeignKey(PersonalClinica, null=False, on_delete=models.CASCADE)
    idOrden = models.ForeignKey(Orden, null=True, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=250,null=True)
    recordatorioSiguienteVisia = models.CharField(max_length=30,null=True)

class Sesion(models.Model):
    id=models.AutoField(primary_key=True)
    usuario=models.ForeignKey(PersonalClinica, on_delete=models.CASCADE, null=True)
    token=models.CharField(max_length=200,null=False,default="")

class Factura(models.Model):
    nfactura = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, null=False, on_delete=models.CASCADE)
    medico = models.ForeignKey(PersonalClinica, null=False, on_delete=models.CASCADE)
    poliza = models.ForeignKey(SeguroPaciente, null=False, on_delete=models.CASCADE)
    fecha = models.DateField(null=False)
    valor = models.FloatField(null=False, blank=False)
    copago = models.FloatField(null=False, blank=False)


