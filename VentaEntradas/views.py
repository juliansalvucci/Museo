from django.http import request
from django.utils.dateparse import parse_datetime
from VentaEntradas.models import Empleado, Entrada, Exposicion, ReservaVisita, Sede, Sesion, Tarifa
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib import messages

# MÉTODO PRINCIPAL 1 (Inicia línea de vida)
def registrarNuevaEntrada(request):

    # Tomo la primera sesión que encuentra el gestor.
    sesion = Sesion.objects.get()

    # Obtenemos los datos necesarios ejecutando las funciones subsiguientes.

    empleadoLogueado = buscarEmpleadoLogueado(
        sesion)  # nombre del empleado actual
    # Mapear nombre de empleado actual a objeto
    empleadoLogueado = Empleado.objects.get(nombre=empleadoLogueado)
    # Obtener fecha y hora actual del servidor
    fechaHoraActual = getFechaHoraActual()
    sedeActual = empleadoLogueado.getSede()  # Obtener el nombre de la sede actual
    tarifas = buscarTarifasSedeEmpleado(empleadoLogueado)

    # Agregar los datos obtenidos en un diccionario.
    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifas': tarifas,
        'sesion': sesion,
        'sedeActual': sedeActual
    }
    # ésto sería equivialente al método "mostrarTarifasVigentes() Y solicitar seleccion tarifa"
    return render(request, "mostrarTarifasVigentes.html", context)


# AUXILIARES
# a partir de la sesion obtengo el empleado logueado
def buscarEmpleadoLogueado(sesion):
    # obtiene el nombre del empleado en sesión haciendo SesionActual->Usuario->Empleado->getNombre()
    return sesion.getEmpleadoEnSesion()


def getFechaHoraActual():  # Obtener fecha y hora actual
    return datetime.now()


# Obtener las tarifas vigentes vinculadas a un empleado
def buscarTarifasSedeEmpleado(empleadoLogueado):
    return empleadoLogueado.getTarifasVigentes()


# MÉTODO PRINCIPAL 2
def tomarTarifasSeleccionadas(request):
    # lo primero que hace el método es justamente "tomar tarifa seleccionada"
    tarifaSeleccionada = request.POST.get('tarifaSeleccionada')
    # tomamos los datos anteriores para mantenerlos siempre mientras sean necesarios en un futuro
    sesion = request.POST.get('sesion')
    sedeActual = request.POST.get('sedeActual')
    fechaHoraActual = request.POST.get('fechaHoraActual')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    cantidadDeEntradas = request.POST.get('cantidadDeEntradas')

    # mapeo para evitar objeto type string object method not found
    sede = Sede.objects.get(nombre=sedeActual)
    duracion = calcularDuracionExposiciones(sede)

    context = {
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifaSeleccionada': tarifaSeleccionada,
        'sesion': sesion,
        'sedeActual': sedeActual,
        'duracion': duracion,
        'cantidadDeEntradas': cantidadDeEntradas
    }
   

    return render(request, "solicitarCantidadEntradas.html", context)

# AUXILIAR
def calcularDuracionExposiciones(sede):
    duracion = sede.calcularDuracionAExposicionVigente()
    return duracion


# MÉTODO PRINCIPAL 3
def tomarCantidadDeEntradasAEmitir(request):
    tarifaSeleccionada = request.POST.get('tarifaSeleccionada')
    sesion = request.POST.get('sesion')
    sedeActual = request.POST.get('sedeActual')
    sede = Sede.objects.get(nombre=sedeActual)
    fechaHoraActual = request.POST.get('fechaHoraActual')
    fechaHoraActual = fechaHoraActual.replace(".", "")
    fechaHoraActual = datetime.strptime(fechaHoraActual, '%b %d, %Y, %I:%M %p')

    empleadoLogueado = request.POST.get('empleadoLogueado')
    duracion = request.POST.get('duracion')
    cantidadDeEntradas = int(request.POST.get('cantidadDeEntradas'))
    
    #FLUJO ALTERNATIVO, EXCESO DE VISITANTES EN SEDE
    if not validarLimiteDeVisitantes(fechaHoraActual, sede, cantidadDeEntradas):
        return render(request,"error.html", {})

       
    
    # no se si lleva como parámetro las tarifas, no se bién cómo funciona el método -- No, no lleva las tarifas, lleva solo la sede, según la sede actual sabe que exposiciónes hay, la tarifa es la misma, solo cambia la tarifa segun el tipoReserva, que creo que eso no les toca
    exposicionVigente = buscarExposicionVigente(sede)
    totalVenta = calcularTotalDeVenta(cantidadDeEntradas, tarifaSeleccionada)

    context = {
        'sedeActual': sedeActual,
        'empleadoLogueado': empleadoLogueado,
        'fechaHoraActual': fechaHoraActual,
        'tarifaSeleccionada': tarifaSeleccionada,
        'sesion': sesion,
        'cantidadDeEntradas': cantidadDeEntradas,
        'duracion': duracion,
        'exposicionVigente': exposicionVigente,
        'totalVenta': totalVenta,
    }

    return render(request, "tomarCantidadDeEntradas.html", context)

# AUXILIARES
def buscarExposicionVigente(sede):
    return sede.obtenerExposiciones()


# Verifica el número de entradas vendidas para ese mismo momento y lo compara con la capacidad de la sede.

def validarLimiteDeVisitantes(fechaHoraActual, sedeActual, cantidadDeEntradas):
    visitantes = 0
    for entrada in Entrada.objects.all():
        if entrada.sonDeFechaYHoraYPerteneceASede(fechaHoraActual):
            visitantes += 1
    if visitantes + cantidadDeEntradas <= sedeActual.getCantMaximaDeVistantes():
        return True
    else:
        return False
   

'''''
def buscarVisitantesEnSede(fechaHoraActual, cantidadDeEntradas):
    visitantes = 0
    for entrada in Entrada.objects.all():
        if entrada.sonDeFechaYHoraYPerteneceASede(fechaHoraActual):
            visitantes += 1
    return visitantes + cantidadDeEntradas
'''''


# Recorrer todas las intancias de reverva y preguntarles si son para fecha y hora sede.
def buscarReservaParaAsistir():
    reservas = []
    for reserva in ReservaVisita.objects.all():
        if reserva.sonParaFechaYHoraSede():
            reservas.append(reserva.getCantidadDeAlumnosConfirmada())
    return reservas


def calcularTotalDeVenta(cantidadDeEntradas, tarifaSeleccionada):
    total = int(cantidadDeEntradas) * float(tarifaSeleccionada)
    return total


# MÉTODO PRINCIPAL 4
def tomarConfirmacionDeVenta(request):
    tarifaSeleccionada = request.POST.get('tarifaSeleccionada')
    cantidadDeEntradas = int(request.POST.get('cantidadDeEntradas'))
    sedeActual = request.POST.get('sedeActual')
    # mapear sede seleccionada a objeto
    sede = Sede.objects.get(nombre=sedeActual)
    fechaHoraActual = request.POST.get('fechaHoraActual')
    fechaHoraActual = fechaHoraActual.replace(".", "")
    fechaHoraActual = datetime.strptime(
        fechaHoraActual, '%b %d, %Y, %I:%M %p')  # parsear string a datetime
    

    # Valores anteriores que no se usan en la generación de la entrada: (se usan solo para imprimir la pantalla final, pero no son necesarios en el crearEntradas())
    sesion = request.POST.get('sesion')
    empleadoLogueado = request.POST.get('empleadoLogueado')
    duracion = request.POST.get('duracion')
    exposicionVigente = request.POST.getlist('exposicionVigente[]')
    totalVenta = request.POST.get('totalVenta')
   


    # obtener el nuevo numero entrada
    ultimoNumEntrada = buscarUltimoNumeroDeEntrada()
    ultimoNumEntrada += 1
    entradasNuevas = generarEntradas(
        cantidadDeEntradas, ultimoNumEntrada, fechaHoraActual, tarifaSeleccionada, sede)

    print(entradasNuevas)

    context = {
        'entradasNuevas': entradasNuevas,
    }

    return render(request, "finCU.html", context)

# AUXILIARES


# Buscar el último número de entrada para sumarle 1
def buscarUltimoNumeroDeEntrada():
    maximo = 0
    nuevoNumero = 0
    for entrada in Entrada.objects.all():
        if entrada.getNumero() > maximo:
            maximo = entrada.getNumero()
            nuevoNumero = maximo + 1
    return nuevoNumero


def generarEntradas(cantidadDeEntradas, ultimoNumEntrada, fechaHoraActual, tarifaSeleccionada, sede):  # for para generar
    nuevasEntradas = []
    for x in range(cantidadDeEntradas):
        entrada = Entrada.objects.create(   #CREACIÓN DE NUEVAS ENTRADAS.
            fechaYHoraVenta=fechaHoraActual,
            monto=tarifaSeleccionada,
            numero=ultimoNumEntrada,
            sede=sede,
            tarifa=sede.tarifa.all().get(monto=tarifaSeleccionada)
        )  # pasar parámetro
        ultimoNumEntrada += 1
        # entrada.save() probar que se crea antes de guardarlo en la base de datos
        nuevasEntradas.append(entrada)
    return nuevasEntradas



def actualizarVisitantesEnPantalla():
    pass

