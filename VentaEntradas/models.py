from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField, DateField, TimeField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _  # conversión de idiomas
from django.contrib.auth.models import User # trae los usuarios logueados en el sistema.
from datetime import date, datetime, timedelta


class Sesion(models.Model):
    fechaInicio = DateField(blank = True, null = True)
    fechaFin = DateField(blank = True, null = True)
    horaInicio = TimeField(blank = True, null = True)
    horaFin = TimeField(blank = True, null = True)
    usuario = ForeignKey(
        "Usuario",
        verbose_name=_('Usuario'),
        related_name= 'usuario',
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
    #Obtener el empleado en sesion
    def getEmpleadoEnSesion(self):  
        return self.usuario.getEmpleado()
        

class Usuario(models.Model):
    nombreUsuario = CharField(max_length=10)
    contraseña = CharField(max_length=10)
    empleado = ForeignKey(
        "Empleado",
        verbose_name=_('empleado'),
        related_name= 'emp',
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )

    def getEmpleado(self):  #obtener el empleado asociado a ese usuario.
        return self.empleado.getNombre()


class Empleado(models.Model):
    apellido = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    codigoValidacion = models.IntegerField(blank = True, null = True)
    cuit = models.IntegerField(blank = True, null = True)
    dni = models.IntegerField(blank = True, null = True)
    calle = models.CharField(max_length=10, blank = True, null = True)
    numero = models.IntegerField(blank = True, null = True)
    fechaIngreso = models.DateField(blank = True, null = True)
    fechaNacimiento = models.DateField(blank = True, null = True)
    mail = models.EmailField(blank = True, null = True)
    telefono = models.IntegerField(blank = True, null = True)
    sede = ForeignKey(
        "Sede",
        verbose_name=_('Sede'),
        related_name= 'sd',
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
    
    def getNombre(self):
        return self.nombre

    def getTarifasVigentes(self):
        return self.sede.getTarifasVigentes()

    def getSede(self):
        return self.sede.getNombre()


class Sede(models.Model):
    horaApetura = models.TimeField(blank = True, null = True)
    horaCierre = models.TimeField(blank = True, null = True)
    diaInicio = DateField(blank = True, null = True)
    diaFin = models.DateField(blank = True, null = True)
    cantMaxVisitantes = models.IntegerField()
    cantMaxPorGuia = models.IntegerField(blank = True, null = True)
    nombre = models.TextField(max_length=200)
    exposicion = models.ManyToManyField("Exposicion",blank = True, null = True)
    tarifa = models.ManyToManyField("Tarifa",blank = True, null = True )
        
    
    def calcularDuracionAExposicionVigente(self):
        duracion = timedelta(0)
        for exposicion in self.exposicion.all(): #se recorren todos los detalles asociados y le pide que ejecute el método para buscar la duración resumida de obras.
            if exposicion.esVigente():
                duracion += exposicion.calcularDuracionDeObrasExpuestas()
        return duracion 


        
    def getCantMaximaDeVistantes(self):
        return self.cantMaxVisitantes

    def getTarifasVigentes(self):
        tarifas = []
        for tarifa in self.tarifa.all():  #Método que solicita colaboración a la clase tarifa para que verifique las tarifas en vigencia.
           
            if tarifa.esVigente(): #un objeto tarifa verifica si es vigente.   
  
                tarifas.append(tarifa)
        return tarifas  #Retorna none cuándo ninguna de las tarifas iteradas es vigente.
    
    def validadCantidadMaximaDeVisitantes(self):
        pass

    def getNombre(self):
        return self.nombre
    

class Tarifa(models.Model):
    fechaInicioVigencia = models.DateField()
    fechaFinVigencia = models.DateField()
    monto = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default = 0
    )
    tipoDeEntrada = models.OneToOneField(
        "TipoDeEntrada",
        verbose_name=_('Tipo de entrada'),
        related_name= 'TipoDeEntrada',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tipoDeVisita = models.OneToOneField(
        "TipoDevisita",
        verbose_name=_('Tipo de visita'),
        related_name= 'TipoDeVisita',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def esVigente(self):  #Método que pregunta a un determinado objeto de tipo Tarifa si es vigente.
        if (self.fechaInicioVigencia <= date.today()) and (self.fechaFinVigencia > date.today()): #date.today = función que retorna la fecha actual.
            return True
        else:
            return False
    
    def getMonto(self):
        return self.monto

    def mostrarDatos(self): #Obtener el monto de la entrada por tipo de entrada y tipo de visita
        montoTarifa = self.monto
        tipoEntrada = self.tipoDeEntrada.getNombre()
        tipoVisita = self.tipoDeVisita.getNombre()
        return (montoTarifa,tipoEntrada,tipoVisita) #recordar que se invoca a partir de los 3 parámetros


class TipoDeEntrada(models.Model): 
    nombre = models.CharField(max_length=200)

    def getNombre(self): #Retorna el nombre un tipo de entrada.
        return self.nombre


class TipoDevisita(models.Model):
    nombre = models.CharField(max_length=200)

    def getNombre(self):  #Retorna el nombre un tipo de visita.
        return self.nombre


class Exposicion(models.Model):
    fechaFin = models.DateField(blank = True, null = True)
    fechaFinReplanificada = models.DateField(blank = True, null = True)
    fechaInicio = models.DateField(blank = True, null = True)
    fechaInicioReplanificada = models.DateField(blank = True, null = True)
    horaApertura = models.TimeField(blank = True, null = True)
    horaCierre = models.TimeField(blank = True, null = True)
    nombre = models.CharField(max_length=200,blank = True, null = True)
    detalleExposicion = models.ManyToManyField("DetalleExposicion",blank = True, null = True)
    empleado = models.OneToOneField(
        "Empleado",
        verbose_name=_('Empleado'),
        related_name='e',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def esVigente(self):
        if (self.fechaInicio <= date.today()) and (self.fechaFin > date.today()):
            return True
        else:
            return False

    def calcularDuracionDeObrasExpuestas(self): 
        duracion = timedelta(0)
        for detalle in self.detalleExposicion.all(): #se recorren todos los detalles asociados y le pide que ejecute el método para buscar la duración resumida de obras.
            duracion += detalle.buscarDuracionResumidaDeObra()
        return duracion  


class DetalleExposicion(models.Model):
    obra = models.OneToOneField(
        "Obra",
        verbose_name=_('Obra'),
        related_name='obr',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def buscarDuracionResumidaDeObra(self): #Método que solicita colaboración a la clase obra para que obtenga la duracion resumida de sus obras. 
        return self.obra.getDuracionResumida()   
        

class Obra(models.Model):
    nombre = models.CharField(max_length=200, unique=True,blank = True, null = True)
    peso = models.IntegerField(blank = True, null = True)
    valuacion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank = True, 
        null = True
    )
    alto = models.IntegerField(blank = True, null = True)
    ancho = models.IntegerField(blank = True, null = True)
    descripcion = models.TextField(blank = True, null = True)
    fechaCreacion = models.DateField(blank = True, null = True)
    fechaPrimerIngreso = models.DateField(blank = True, null = True)
    duracionExtendida = models.DurationField(blank = True, null = True)
    duracionResumida = models.DurationField(blank = True, null = True)
    
    def getDuracionResumida(self): #Método para obtener la duración resumida de una determinada obra.
        return self.duracionResumida 


class Entrada(models.Model):
    fechaYHoraVenta = models.DateTimeField(blank = True, null = True)
    monto = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default = 0,
        blank = True, 
        null = True
    )
    numero = models.IntegerField()
    sede = models.ForeignKey(
        "Sede",
        verbose_name=_('Sede'),
        related_name= 'sede',
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
    tarifa = models.ForeignKey(
        "Tarifa",
        verbose_name=_('Tarifa'),
        related_name= 'tarifa',
        on_delete=models.SET_NULL,
        blank = True,
        null = True    
    )
    def getNumero(self):
        return self.numero

    def sonDeFechaYHoraYPerteneceASede(self,fechaHoraActual):
        if (self.fechaYHoraVenta <= fechaHoraActual) and (self.fechaYHoraVenta > fechaHoraActual):
            return True
        else:
            return False 

    def getMonto(self):
        return self.monto

    #def __init__(self): #completar parámetros
        #self.numero = 0
        

class ReservaVisita(models.Model):
    cantidadAlumnos = models.IntegerField(blank = True, null = True)
    cantidadAlumnosConfirmada = models.IntegerField(blank = True, null = True)
    duracionEstimada = models.IntegerField(blank = True, null = True)
    fechaHoraCreacion = models.DateTimeField(blank = True, null = True)
    fechaHoraReserva = models.DateTimeField(blank = True, null = True)
    fechaYHoraInicioReal = models.DateTimeField(blank = True, null = True)
    fechaYHoraFinReal = models.DateTimeField(blank = True, null = True)
    numeroReserva = models.IntegerField()
    sede = models.ForeignKey(
        "Sede",
        verbose_name=_('Sede'),
        related_name= 'Sede',
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
    
    def sonParaFechaYHoraSede(self,fechaHoraActual):
        if (self.horaInicioReal <= fechaHoraActual) and (self.fechaFinReal > fechaHoraActual):
            return True
        else:
            return False 
        
    def getCantidadDeAlumnosConfirmada(self):
        return self.cantidadAlumnosConfirmada


        










