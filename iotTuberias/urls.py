from django.urls import path
from . import views

app_name="iotTuberias"

urlpatterns = [
    path("",views.index,name="index"),
    path("registrarDatos",views.registrarDatos,name='registrarDatos'),
    path("enviarDatos",views.enviarDatos,name='enviarDatos'),
    path("descargarDatos",views.descargarDatos,name='descargarDatos'),
]