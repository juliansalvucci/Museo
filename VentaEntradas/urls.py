from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name='VentaEntradas'

urlpatterns = [
    path('registrarNuevaEntrada/', views.registrarNuevaEntrada),
    path('buscarEmpleadoLogueado/', views.buscarCapacidadSede),
    path('getFechaHoraActual/', views.buscarEmpleadoLogueado),
    path('buscarTarifasSedeEmpleado/', views.buscarExposicionVigente),
    path('tomarTarifasSeleccionadas/', views.buscarReservaParaAsistir),
    path('buscarExposicionVigente/', views.buscarTarifaSedeEmpleado),
    path('validarLimiteDeVisitantes/', views.calcularDuracionVisitaCompleta),
    path('buscarVisitantesEnSede/', views.generarEntradas),
    path('buscarReservaParaAsistir/', views.obtenerFechaActual),
    path('calcularTotalDeVenta/', views.validarLimiteDeVisitantes),
    path('buscarUltimoNumeroDeEntrada/', views.buscarVisitantesEnSede),
    path('generarEntradas/', views.calcularTotalDeVenta),
    path('imprimirEntrada/', views.buscarUltimoNumeroDeEntrada),
    path('actualizarVisitantesEnPantalla/', views.getEmpleadoEnSesion),
    path('finCu/', views.tomarConfirmacionDeVenta),
]