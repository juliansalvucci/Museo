from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name='VentaEntradas'

urlpatterns = [
    path('registrarNuevaEntrada/', views.registrarNuevaEntrada),
    path('buscarCapacidadSede/', views.buscarCapacidadSede),
    path('buscarEmpleadoLogueado/', views.buscarEmpleadoLogueado),
    path('buscarExposicionVigente/', views.buscarExposicionVigente),
    path('buscarReservaParaAsistir/', views.buscarReservaParaAsistir),
    path('buscarTarifaSedeEmpleado/', views.buscarTarifaSedeEmpleado),
    path('calcularDuracionVisitaCompleta/', views.calcularDuracionVisitaCompleta),
    path('generarEntradas/', views.generarEntradas),
    path('obtenerFechaActual/', views.obtenerFechaActual),
    path('validarLimiteDeVisitantes/', views.validarLimiteDeVisitantes),
    path('buscarVisitantesEnSede/', views.buscarVisitantesEnSede),
    path('calcularTotalDeVenta/', views.calcularTotalDeVenta),
    path('buscarUltimoNumeroDeEntrada/', views.buscarUltimoNumeroDeEntrada),
    path('getEmpleadoEnSesion/', views.getEmpleadoEnSesion),
    path('tomarConfirmacionDeVenta/', views.tomarConfirmacionDeVenta),
]