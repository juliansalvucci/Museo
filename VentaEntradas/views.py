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
    return empleadoLogueado.getTarifaVigente()

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

def buscarExposicionVigente(sede):
    duracion = sede.calcularDuracionAExposicionVigente()
    return duracion
    
    
def validarLimiteDeVisitantes(request):
    capacidadSede = Sede.getCantMaximaDeVistantes
    visitantes = ReservaVisita.sonParaFechaYHoraSede

    if capacidadSede < visitantes:
        print("Límite de visitantes excedido")
   
def buscarVisitantesEnSede(request):
    pass


def buscarReservaParaAsistir(request,id):
    for reservas in ReservaVisita.all():
        if ReservaVisita.sonParaFechaYHoraSede():
            return reservas
    return None


def calcularTotalDeVenta(request):
    total = 0
    for entradas in Entrada.all():
        total = Entrada.monto
    return total

def buscarUltimoNumeroDeEntrada(request):
    pass

def generarEntradas(request):
    context = {}
    return render(request,"index.html",context)

def imprimirEntrada(request):
    pass

def actualizarVisitantesEnPantalla():
    pass

def finCu():
    pass




    









        



    







