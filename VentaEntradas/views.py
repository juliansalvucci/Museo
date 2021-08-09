from django.http import request
from VentaEntradas.models import Empleado, Entrada, Exposicion, ReservaVisita, Sede, Sesion, Tarifa
from django.shortcuts import render
from datetime import datetime

#MÉTODO PRINCIPAL(Inicia línea de vida)
def registrarNuevaEntrada(request):

    sesion = 1
    sesion = Sesion.objects.get(pk=1) #Tomo la sesión vigente.

    # obtenemos los datos necesarios ejecutando las funciones subsiguientes.
    empleadoLogueado = Empleado.objects.get()
    empleadoLogueado = buscarEmpleadoLogueado(sesion) 
    fechaHoraActual = getFechaHoraActual()
    tarifas = Tarifa.objects.get()
    tarifas = buscarTarifasSedeEmpleado(sesion)
    sedeActual = empleadoLogueado.getSede()
    
    
    # metemos los datos obtenidos en un diccionario.
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifas': tarifas,
        'sesion': sesion,
        'sedeActual': sedeActual
    }
    return render(request,"mostrarTarifasVigentes.html", context) # ésto sería equivialente al método "mostrarTarifasVigentes() Y solicitar seleccion tarifa"


    
#AUXILIARES
def buscarEmpleadoLogueado(sesion): #a partir de la sesion obtengo el empleado logueado
    return sesion.getEmpleadoEnSesion()

def getFechaHoraActual(): #Obtener fecha y hora actual
    return datetime.now()

def buscarTarifasSedeEmpleado(sesion):  #Obtener las tarifas vigentes vinculadas a un empleado
    empleadoLogueado = sesion.getEmpleadoEnSesion()
    return empleadoLogueado.getTarifasVigentes()

#MÉTODO PRINCIPAL
def tomarTarifasSeleccionadas(request):
    #lo primero que hace el método es justamente "tomar tarifa seleccionada"
    tarifaSeleccionada = request.POST.get('tarifaSeleccionada') # 
    # tomamos los datos anteriores para mantenerlos siempre mientras sean necesarios en un futuro
    sesion = request.POST.get('sesion')
    sedeActual = request.POST.get('sedeActual')
    fechaHoraActual = request.POST.get('fechaHoraActual')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    
    #mapeo para evitar objeto type string object method not found
    sede = Sede.objects.get(nombre = sedeActual)
    duracion = buscarExposicionVigente(sede)

    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifaSeleccionada': tarifaSeleccionada,
        'sesion': sesion,
        'sedeActual': sedeActual,
        'duracion': duracion
    }
    #fijate que context envía los datos que calcula (exposicion vigente) y arrastra también todos los datos viejos que vienen de las pantallas anteriores.

    return render(request, "solicitarCantidadEntradas.html", context)

#AUXILIAR
def buscarExposicionVigente(sede):
    duracion = sede.calcularDuracionAExposicionVigente()
    return duracion


#MÉTODO PRINCIPAL
def tomarCantidadDeEntradasAEmitir(request):
      
    tarifaSeleccionada = request.POST.get('tarifaSeleccionada') 
    cantidadDeEntradas = request.POST.get('cantidadDeEntradas')
    sesion = request.POST.get('sesion')
    sedeActual = request.POST.get('sedeActual')
    fechaHoraActual = request.POST.get('fechaHoraActual')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    duracion = request.POST.get('duracion')
    if not validarLimiteDeVisitantes(fechaHoraActual,sedeActual): #Si no puede entrar
        return (render,"Error.html", {}) 
    exposicionVigente = buscarExposicionVigente(Sede) #no se si lleva como parámetro las tarifas, no se bién cómo funciona el método
    
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifaSeleccionada': tarifaSeleccionada,
        'sesion': sesion,
        'cantidadDeEntradas': cantidadDeEntradas,
        'duracion': duracion,
        'exposicionVigente': exposicionVigente
    }

    return render(request, "solicitarCantidadEntradas.html", context)


#AUXILIARES
def validarLimiteDeVisitantes(fechaHoraActual,sede): #Verifica el número de entradas vendidas para ese mismo momento y lo compara con la capacidad de la sede.
    visitantes = 0
    for entrada in Entrada.objects.all():
        if entrada.sonDeFechaYHoraYPerteneceASede(fechaHoraActual,sede):
            visitantes +=1
    if visitantes <= sede.getCantMaximaDeVistantes():
        return True
    else:
        return False

    
def buscarReservaParaAsistir(): #Recorrer todas las intancias de reverva y preguntarles si son para fecha y hora sede.
    reservas = []
    for reserva in ReservaVisita.objects.all():
        if reserva.sonParaFechaYHoraSede():
            reservas.append(reserva.getCantidadDeAlumnosConfirmada())
    return reservas


def calcularTotalDeVenta(cantidadDeEntradas,tarifaSeleccionada):
    total = cantidadDeEntradas * tarifaSeleccionada
    return total


#MÉTODO PRINCIPAL
def tomarConfirmacionDeVenta(request):
    tarifaSeleccionada = request.POST.get('tarifaSeleccionada')  
    cantidadDeEntradas = request.POST.get('cantidadDeEntradas')
    sesion = request.POST.get('sesion')
    sedeActual = request.POST.get('sedeActual')
    fechaHoraActual = request.POST.get('fechaHoraActual')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    duracion = request.POST.get('duracion')
    if not validarLimiteDeVisitantes(fechaHoraActual,sedeActual): #Si no puede entrar
        return (render,"Error.html", {}) 
    exposicionVigente = buscarExposicionVigente(Sede) #no se si lleva como parámetro las tarifas, no se bién cómo funciona el método
    
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifaSeleccionada': tarifaSeleccionada,
        'sesion': sesion,
        'cantidadDeEntradas': cantidadDeEntradas,
        'duracion': duracion,
        'exposicionVigente': exposicionVigente
    }

    return render(request, "solicitarCantidadEntradas.html", context)

#AUXILIARES
def buscarUltimoNumeroDeEntrada(entrada): #Buscar el último número de entrada para sumarle 1
    maximo = 0
    nuevoNumero = 0
    for entrada in Entrada.objects.all():
        if entrada.getNumero() > maximo:
            maximo = entrada.getNumero()
            nuevoNumero = maximo + 1
    return nuevoNumero 


def generarEntradas(cantidadDeEntradas):  #for para generar 
    nuevasEntradas = []
    for x in range(cantidadDeEntradas):
       entrada = Entrada.objects.create()  #pasar parámetro
       #entrada.save() probar que se crea antes de guardarlo en la base de datos
       nuevasEntradas.append(entrada)
    return nuevasEntradas 
    


def imprimirEntrada(request): #pasar por context nuevas entradas
    entradas = generarEntradas(cantidadDeEntradas)


def actualizarVisitantesEnPantalla(): #Varios mensajes 
    pass

def finCu():
    pass




    









        



    







