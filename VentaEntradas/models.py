from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField, DateField, TimeField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _  # conversión de idiomas
from django.contrib.auth.models import User # trae los usuarios logueados en el sistema.
from datetime import date


class Sesion(models.Model):
    fechaInicio = DateField(
        _('fechaInicio'),
        help_text=_('fecha de inicio de sesión'),
    )
    fechaFin = DateField(
        _('fechaFin'),
        help_text=_('fecha de fin de sesion'),
    )
    horaInicio = TimeField(
        _('horaInicio'),
        help_text=_('hora de inicio de sesion'),
    )
    horaFin = TimeField(
        _('horaFin'),
        help_text=_('hora de fin de sesion'),
    )
    usuario = ForeignKey(
        "Usuario",
        verbose_name=_('Usuario'),
        help_text=_('Usuario'),
        related_name= 'usuario',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def getEmpleadoEnSesion(self):
        self.usuario.getEmpleado()


class Usuario(models.Model):
    nombre = CharField(
        _('nombre'),
        help_text=_('nombre de usuario'),
    )
    contraseña = CharField(
        _('contraseña'),
        help_text=_('contraseña de usuario'),
    )
    empleado = ForeignKey(
        "Empleado",
        verbose_name=_('empleado'),
        help_text=_('Empleado'),
        related_name= 'emp',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )

    def getEmpleado(self):
        return self.empleado.getNombre()


class Empleado(models.Model):
    apellido = models.TextField(
        _('apellido'),
        help_text=_('Apellido de empleado'),
        max_length=200,
    )
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de empleado'),
        max_length=200,
    )
    codigoValidacion = models.IntegerField(
        _('CodigoValidacion'),
        help_text=_('Código de validación'),
    )
    cuit = models.IntegerField(
        _('cuit'),
        help_text=_('CUIT'),
        unique=True
    )
    dni = models.IntegerField(
        _('dni'),
        help_text=_('DNI'),
    )
    calle = models.TextField(
        _('calle'),
        help_text=_('Calle'),
        max_length=200,
    )
    numero = models.IntegerField(
        _('numero'),
        help_text=_('Número'),
    )
    fechaIngreso = models.DateField(
        _('fechaIngreso'),
        help_text=_('Fecha de ingreso'),
    )
    fechaNacimiento = models.DateField(
        _('fechaNacimiento'),
        help_text=_('Fecha de nacimiento'),
    )
    mail = models.EmailField(
        _('mail'),
        help_text=_('Mail')
    )
    telefono = models.IntegerField(
        _('telefono'),
        help_text=_('Telefono')
    )
    sede = ForeignKey(
        "Sede",
        verbose_name=_('Sede'),
        help_text=_('Sede'),
        related_name= 'sd',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    
    def getNombre(self):
        return self.nombre
    def getTarifasVigentes(self):
        tarifas = Sede.objects.filter(Sede = self.pk).getTarifasVigentes()


class Sede(models.Model):
    horaApetura = models.TimeField(
        _('horaApetura'),
    )
    horaCierre = models.TimeField()
    diaInicio = DateField()
    diaFin = models.DateField()
    cantMaxVisitantes = models.IntegerField(
        _('cantMaxiVistantes'),
        help_text='Cantidad máxima de Vistantes'
    )
    cantMaxVisitantes = models.IntegerField(
        _('cantMaxiVistantes'),
        help_text='Cantidad máxima de Vistantes'
    )
    cantMaxPorGuia = models.IntegerField(
        _('cantMaxPorGuia'),
        help_text='Cantidad máxima de Vistantes por guía'
    )
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de la sede'),
        max_length=200,
    )
    exposicion = models.ForeignKey(
        "Exposicion",
        verbose_name=_('Exposición'),
        help_text=_('Exposición'),
        related_name= 'Exposición',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tarifa = models.ForeignKey(
        "Tarifa",
        verbose_name=_('Tarifa'),
        help_text=_('Tarifa'),
        related_name= 'tar',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def buscarDuracionDeExposiciones(self):
        exposiciones = Exposicion.object.filter(exposicion=self.pk)
        return exposiciones

    def buscarExposiciones(self,Exposicion): 
        exposiciones = Exposicion.object.filter(exposicion=self.pk)
        return exposiciones
        
    
    def calcularDuracionAExposicionVigente(self):
        return self.exposicion.calcularDuracionDeObrasExpuestas()
        
    def getCantMaximaDeVistantes(self):
        return self.cantMaxVisitantes

    def getTarifas(self):
        tarifas = self.tarifa.all()
        return tarifas

    def getTarifasVigentes(self):
        for tarifa in self.tarifa.all():  #Método que solicita colaboración a la clase tarifa para que verifique las tarifas en vigencia.
            if tarifa.esVigente(): #un objeto tarifa verifica si es vigente.   
                return tarifa   #retorna la tarifa vigente.
        return None  #Retorna none cuándo ninguna de las tarifas iteradas es vigente.


class Tarifa(models.Model):
    fechaInicioVigencia = models.DateField(
        _('FechaIncioVigencia'),
        help_text='Fecha de incio de vigencia'
    )
    fechaFinVigencia = models.DateField(
        _('fechaFinVigencia'),
        help_text='Fecha de fin de vigencia',
    )
    monto = models.DecimalField(
        _('monto'),
        help_text=_('Monto de la tarifa'),
        max_digits=15, 
        decimal_places=2,
        default = 0
    )
    tipoDeEntrada = models.OneToOneField(
        "TipoDeEntrada",
        verbose_name=_('Tipo de entrada'),
        help_text=_('Tipo de entrada'),
        related_name= 'TipoDeEntrada',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tipoDeVisita = models.OneToOneField(
        "TipoDevisita",
        verbose_name=_('Tipo de visita'),
        help_text=_('Tipo de visita'),
        related_name= 'TipoDeVisita',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def esVigente(self):  #Método que pregunta a un determinado objeto de tipo Tarifa si es vigente.
        if (self.fechaInicioVigencia >= date.today()) and (self.fechaFinVigencia < date.today()): #date.today = función que retorna la fecha actual.
            return True
        else:
            return False
            
    def getMonto(self):
        return self.monto  #Método que retorna el monto de una determinada tarifa.


class TipoDeEntrada(models.Model): 
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de tipo de entrada'),
        max_length=200,
    )

    def getNombre(self): #Retorna el nombre un tipo de entrada.
        return self.nombre


class TipoDevisita(models.Model):
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de tipo de visita'),
        max_length=200,
    )

    def getNombre(self):  #Retorna el nombre un tipo de visita.
        return self.nombre


class Exposicion(models.Model):
    fechaFin = models.DateField(
        _('fechafin'),
        help_text='Fecha de fin',
        blank=True
    )
    fechaFinReplanificada = models.DateField(
        _('fechaFinReplanificada'),
        help_text='Fecha de fin replanificada',
        blank=True
    )
    fechaInicio = models.DateField(
        _('fechaInicio'),
        help_text='Fecha de inicio'
    )
    fechaInicioReplanificada = models.DateField(
        _('fechaInicioReplanificada'),
        help_text='Fecha de inicio replanificada'
    )
    horaApertura = models.TimeField(
        _('horaApertura'),
        help_text='Hora de apertura'
    )
    horaCierre = models.TimeField(
        _('horaCierre'),
        help_text='Hora de cierre'
    )
    nombre = models.CharField(
        _('nombre'),
        help_text=_('Nombre de exposición'),
        max_length=200,
    )
    detalleExposicion = models.ForeignKey(
        "DetalleExposicion",
        verbose_name=_('Detalle Exposición'),
        help_text=_('Detalle Exposición'),
        related_name='dt',
        on_delete=models.CASCADE, #Al borrar el detalle, borrar la exposición. (Agregación)
        blank=False,
        null=True
    )
    empleado = models.OneToOneField(
        "Empleado",
        verbose_name=_('Empleado'),
        help_text=_('Empleado'),
        related_name='e',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )

    def esVigente(self):
        if (self.fechaInicio or self.fechaInicioReplanificada >= date.today) and (self.fechaFin or self.fechaFinReplanificada < date.today()):
            return True
        else:
            return False

    def calcularDuracionDeObrasExpuestas(self):
        detalles = DetalleExposicion.object.filter(detalleExposicion=self.pk) #se crea la variable "detalles" la cual contiene todos los objetos de DetalleExposición mediante el puntero. 
        duracion = 0
        for detalle in detalles: #se recorren todos los detalles asociados y le pide que ejecute el método para buscar la duración resumida de obras.
            duracion += detalle.buscarDuracionResumidaDeObra()
        return duracion  


class DetalleExposicion(models.Model):
    obra = models.OneToOneField(
        "Obra",
        verbose_name=_('Obra'),
        help_text=_('Obra'),
        related_name='obr',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )

    def buscarDuracionResumidaDeObra(self): #Método que solicita colaboración a la clase obra para que obtenga la duracion resumida de sus obras. 
        return self.obra.getDuracionResumida()   
        

class Obra(models.Model):
    nombre = models.CharField(
        _('nombre'),
        help_text=_('Nombre de la obra'),
        max_length=200,
        unique=True   
    )
    peso = models.IntegerField(
        _('peso'),
        help_text=_('Peso en kg')
    )
    valuacion = models.DecimalField(
        _('valuación'),
        help_text=_('Valuación en pesos'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    alto = models.IntegerField(
        _('alto'),
        help_text=_('Alto de la obra')
    )
    ancho = models.IntegerField(
        _('ancho'),
        help_text=_('Ancho de la obra')
    )
    descripcion = models.TextField(
        _('descripción'),
        help_text=_('Descripción de la obra')
    )
    fechaCreacion = models.DateField(
        _('FechaCreacion'),
        help_text=_('Fecha de creación de la obra')
    )
    fechaPrimerIngreso = models.DateField(
        _('FechaPrimerIngreso'),
        help_text=_('Fecha de primer ingreso de la obra')
    )
    duracionExtendida = models.DurationField(
        _('DuracionExtendida'),
        help_text=_('Duración extendida')
    )
    duracionResumida = models.DurationField(
        _('DuracionResumida'),
        help_text=_('Duración resumida')
    )
    

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return '{}'.format(self.nombre)

    def getDuracionResumida(self): #Método para obtener la duración resumida de una determinada obra.
        return self.duracionResumida 


class Entrada(models.Model):
    fechaVenta = models.DateField(
        _('fechaVenta'),
        help_text='Fecha de venta'
    )
    horaVenta = models.TimeField(
        _('horaVenta'),
        help_text='Hora de venta'
    )
    monto = models.DecimalField(
        _('monto'),
        help_text=_('Monto de la entrada'),
        max_digits=15, 
        decimal_places=2,
        default = 0
    )
    numero = models.IntegerField(
        _('numero'),
        help_text='Numero de entrada'
    )
    sede = models.ForeignKey(
        "Sede",
        verbose_name=_('Sede'),
        help_text=_('Sede'),
        related_name= 'sede',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tarifa = models.ForeignKey(
        "Tarifa",
        verbose_name=_('Tarifa'),
        help_text=_('Tarifa'),
        related_name= 'tarifa',
        on_delete=models.SET_NULL,
        blank = False,
        null = True    
    )
    def getNumero(self):
        return self.numero


class ReservaVisita(models.Model):
    cantidadAlumnos = models.IntegerField(
        _('cantidadAlumnos'),
        help_text=_('Cantidad de alumnos'),
    )
    cantidadAlumnosConfirmada = models.IntegerField(
        _('cantidadAlumnosConfirmada'),
        help_text=_('Cantidad de alumnos confirmada'),
    )
    duracionEstimada = models.IntegerField(
        _('duracionEstimada'),
        help_text=_('Duración estimada'),
    )
    fechaHoraCreacion = models.DateTimeField(
        _('fechaHoraCreacion'),
        help_text=_('Fecha y hora de creación'),
    )
    fechaHoraReserva = models.DateTimeField(
        _('fechaHoraReserva'),
        help_text=_('Fecha y hora de reserva'),
    )
    horaInicioReal = models.TimeField(
        _('horaInicioReal'),
        help_text=_('Hora de inicio real'),
    )
    horaFinReal = models.TimeField(
        _('horaFinReal'),
        help_text=_('Hora de fin real'),
    )
    numeroReserva = models.IntegerField(
        _('numeroRserva'),
        help_text=_('Numero de reserva'),
    )
    sede = models.ForeignKey(
        "Sede",
        verbose_name=_('Sede'),
        help_text=_('Sede'),
        related_name= 'Sede',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def obtenerAlumnosEnReserva(self):
        return self.cantidadAlumnosConfirmada
    def sonParaFechaYHoraSede(self):
        if (self.horaInicioReal >= self.sede.horaApertura) and (self.fechaFinReal < self.sede.horaCierre):
            return True
        else:
            return False 
        










