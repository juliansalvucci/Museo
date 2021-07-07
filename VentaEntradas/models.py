from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import NullBooleanField
from django.utils.translation import ugettext_lazy as _  # conversión de idiomas
# trae los usuarios logueados en el sistema.
from django.contrib.auth.models import User
from datetime import date


class TipoDeEntrada(models.Model):
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de tipo de entrada'),
        max_length=200,
    )

    def getNombre(self):
        return self.nombre


class TipoDevisita(models.Model):
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de tipo de visita'),
        max_length=200,
    )

    def getNombre(self):
        return self.nombre


class DetalleExposicion(models.Model):
    obra = models.OneToOneField(
        Obra,
        verbose_name=_('Obra'),
        help_text=_('Obra'),
        related_name='obr',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )

    def buscarDuracionResumidaDeObra(self):
        return self.obra.getDuracionResumida()


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
    nombre = models.TextField(
        _('nombre'),
        help_text=_('Nombre de exposición'),
        max_length=200,
    )
    empleado = models.OneToOneField(
        Empleado,
        verbose_name=_('Empleado'),
        help_text=_('Empleado'),
        related_name='Empleado',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    detalleExposicion = models.ForeignKey(
        DetalleExposicion,
        verbose_name=_('Detalle Exposición'),
        help_text=_('Detalle Exposición'),
        related_name='dt',
        on_delete=models.CASCADE 
        blank=False,
        null=True
    )

    def esVigente(self):
        if (self.fechaInicio or self.fechaInicioReplanificada >= date.today) and (self.fechaFin or self.fechaFinReplanificada < date.today()):
            return True
        else:
            return False

    def calcularDuracionDeObrasExpuestas(self, detalleExposicion):
        detalles = detalleExposicion.object.filter(detalleExposicion=self.pk)
        duracion = 0
        for detalleExposicion in detalles:
            duracion += detalleExposicion.buscarDuracionResumidaDeObra()
        return duracion


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
        TipoDeEntrada,
        verbose_name=_('Tipo de entrada'),
        help_text=_('Tipo de entrada'),
        related_name= 'TipoDeEntrada',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tipoDeVisita = models.OneToOneField(
        TipoDevisita,
        verbose_name=_('Tipo de visita'),
        help_text=_('Tipo de visita'),
        related_name= 'TipoDeVisita',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def esVigente(self):
        if (self.fechaInicioVigencia >= date.today()) and (self.fechaFinVigencia < date.today()):
            return True
        else:
            return False
            
    def getMonto(self):
        return self.monto


class Sede(models.Model):
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
        Exposicion,
        verbose_name=_('Exposición'),
        help_text=_('Exposición'),
        related_name= 'Exposición',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tarifa = models.ForeignKey(
        Tarifa,
        verbose_name=_('Tarifa'),
        help_text=_('Tarifa'),
        related_name= 'tar',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    def buscarDuracionDeExposiciones(self,Exposicion):
        exposiciones = Exposicion.object.filter(exposicion=self.pk)
        duracion = 0
        for Exposicion in exposiciones:
            duracion += Exposicion.calcularDuracionDeObrasExpuestas()
        return duracion

    def buscarExposiciones(self,Exposicion):
        exposiciones = Exposicion.object.filter(exposicion=self.pk)
        return exposiciones
        
    
    def calcularDuracionAExposicionesVigentes(self,Exposicion):
        pass
    def getCantMaximaDeVistantes(self):
        return self.cantMaxVisitantes
    def getTarifas(self,Tarifa):
        return Tarifa
    def getTarifasVigentes(self,Tarifa):
        return Tarifa.esVigente()

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
        help_text=_('Mail'),
    )
    telefono = models.IntegerField(
        _('telefono'),
        help_text=_('Telefono'),
    )
    sede = models.ForeignKey(
        Sede,
        verbose_name=_('sede'),
        help_text=_('sede'),
        related_name= 'sede',
        on_delete=models.SET_NULL,
        blank = False,
        null = True

    )
    def getNombre(self):
        return self.nombre
    def getTarifasVigentes(self,sede):
        return sede.getTarifasVigentes()



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
        Sede,
        verbose_name=_('Sede'),
        help_text=_('Sede'),
        related_name= 'sede',
        on_delete=models.SET_NULL,
        blank = False,
        null = True
    )
    tarifa = models.ForeignKey(
        Tarifa,
        verbose_name=_('Tarifa'),
        help_text=_('Tarifa'),
        related_name= 'tarifa',
        on_delete=models.SET_NULL,
        blank = False,
        null = True    
    )
    def getNumero(self):
        return self.numero
    


class Obra(models.Model):
    nombre = models.CharField(
        _('nombre'),
        help_text=_('Nombre de la obra'),
        max_length=200,
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
    empleado = models.OneToOneField(
        Empleado,
        verbose_name=_('Empleado'),
        help_text=_('Empleado'),
        related_name= 'emp',
        on_delete=models.SET_NULL,
        blank = False,
        null = True   

    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return '{}'.format(self.nombre)

    def getDuracionResumida(self):
        return self.duracionResumida


        
        

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
        Sede,
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
        pass





'''
class DetalleExposicion(models.Model):
.... #acá pondrías los atributos/camos
.... def getDuracionExposicion():
........ obras = Obras.object.filter(puntero=self.pk)
........ duracion = 0
........ for obra in obras:
............ duracion += obra.getDuracion()
........ return duracion

[11:56, 6/7/2021] Ema $V1ll4sus0: donde dice "puntero" ahi pone vos 
el nombre del campo/atributo que le pusiste al puntero, y vas a ver que dice = self.pk, self.pk significa
 el valor del campo de la clave primaria del objeto actual (DetalleExpo), por lo tanto esa linea 
 completa lo que hace es devolverte el listado de obras filtrando solo las que el puntero apunte al 
 detalle que tenés seleccionado (osea al objeto de la clase detalle expo actual)
´´´

