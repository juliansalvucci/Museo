from datetime import DateTimeField
from VentaEntradas.models import Empleado, Entrada, Exposicion, ReservaVisita, Sede
from django.shortcuts import render

#MÉTODO PRINCIPAL
def registrarNuevaEntrada(request):
    # agarrar datos vía POST
    sesion = request.POST.get('sesion') # acá te tengo que comentar algo pero lo hacemos en la llamada. Ésto depende de si haces una clase sesion o usas una propia.
    
    # obtenemos los datos necesarios ejecutando las funciones
    empleadoLogueado = buscarEmpleadoLogueado(sesion)
    fechaHoraActual = getFechaHoraActual()
    tarifas = buscarTarifasSedeEmpleado(empleadoLogueado)
    

    # metemos los datos obtenidos en un diccionario
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifas': tarifas,
        'sesion': sesion,
    }
    return render(request, "mostrarTarifasVigentes.html", context) # ésto sería equivialente al método "mostrarTarifasVigentes() Y solicitar seleccion tarifa"


    
#AUXILIARES
def buscarEmpleadoLogueado(sesion):
    return sesion.getEmpleadoEnSesion()

def getFechaHoraActual():
    return DateTimeField.now()

def buscarTarifasSedeEmpleado(empleadoLogueado):
    return empleadoLogueado.getTarifasVigentes()

#MÉTODO PRINCIPAL
def tomarTarifasSeleccionadas(request):
    #lo primero que hace el método es justamente "tomar tarifa seleccionada"
    tarifas = request.POST.getlist('tarifas[]') # se escribe así ya que es una lista (vector) con varias tarifas seleccionadas
    # tomamos los datos anteriores para mantenerlos siempre mientras sean necesarios en un futuro
    sesion = request.POST.get('sesion')
    fechaHoraActual = request.POST.get('fechaHoraActual')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    duracion = buscarExposicionVigente('sede')

    exposicionVigente = buscarExposicionVigente(Sede) #no se si lleva como parámetro las tarifas, no se bién cómo funciona el método
    
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifas': tarifas,
        'sesion': sesion,
    }
    #fijate que context envía los datos que calcula (exposicion vigente) y arrastra también todos los datos viejos que vienen de las pantallas anteriores.

    return render(request, "solicitarCantidadEntradas.html", context)

#AUXILIAR
def buscarExposicionVigente(sede):
    duracion = sede.calcularDuracionAExposicionVigente()
    return duracion


#MÉTODO PRINCIPAL
def tomarCantidadDeEntradasAEmitir(request):
      
    tarifas = request.POST.getlist('tarifas[]') 
    sesion = request.POST.get('sesion')
    fechaHoraActual = request.POST.get('fechaHoraActual')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    duracion = buscarExposicionVigente('sede')
    exposicionVigente = buscarExposicionVigente(Sede) #no se si lleva como parámetro las tarifas, no se bién cómo funciona el método
    
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifas': tarifas,
        'sesion': sesion,
    }
    #fijate que context envía los datos que calcula (exposicion vigente) y arrastra también todos los datos viejos que vienen de las pantallas anteriores.

    return render(request, "solicitarCantidadEntradas.html", context)


#AUXILIARES
def validarLimiteDeVisitantes(): #Verifica el númeor de entradas vendidas para ese mismo momento y lo compara con la capacidad de la sede.
    visitantes = []
    for entrada in Entrada.all():
        if Entrada.sonDeFechaYHoraYPerteneceASede():
            visitantes.append(Entrada)
    if visitantes.len() < Sede.getCantMaximaDeVistantes():
        return True

    
def buscarVisitantesEnSede(): #Obtener cantidad de visitantes en la sede
    visitantes = []
    for entrada in Entrada.all():
        if Entrada.sonDeFechaYHoraYPerteneceASede():
            visitantes.append(Entrada)
    return visitantes.len()


def buscarReservaParaAsistir(): #Recorrer todas las intancias de reverva y preguntarles si son para fecha y hora sede.
    reservas = []
    for reserva in ReservaVisita.all():
        if ReservaVisita.sonParaFechaYHoraSede():
            reservas.append(ReservaVisita)
    if reservas.len() < Sede.getCantMaximaDeVistantes():
        return True


def calcularTotalDeVenta():
    total = 0
    for entradas in Entrada.all():
        total = Entrada.getMonto()
    return total


#MÉTODO PRINCIPAL
def tomarConfirmacionDeVenta():
    pass

#AUXILIARES
def buscarUltimoNumeroDeEntrada(): #Buscar el último número de entrada para sumarle 1
    entradas = []
    for entrada in Entrada.all():
        Entrada.getNumero()
    return numero


def generarEntradas():
    pass

def imprimirEntrada():
    pass

def actualizarVisitantesEnPantalla(): #Varios mensajes 
    pass

def finCu():
    pass




    









        



    







