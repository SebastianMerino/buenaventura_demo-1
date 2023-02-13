from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import subprocess
from .models import estadoVehiculo
import datetime
import csv

subprocess.Popen(["python", "pruebaMQTT.py"])

# Create your views here.
def index(request):
    return render(request,"iotVehiculos/index.html")

def registrarDatos(request):
    datoMensaje = str(request.GET.get('mensaje'))
    datoTiempo = str(request.GET.get('tiempo'))
    timestamp = datetime.datetime.strptime(datoTiempo,"%Y-%m-%dT%H:%M:%S"),
    if datoMensaje == 'N':
        datoMensaje = '0'
    elif datoMensaje == 'Y':
        datoMensaje = '1'
    else:
        return JsonResponse({ 'resp':'ok' })

    estadoVehiculo(registroTiempo=datoTiempo,registroInformacion=datoMensaje).save()
    return JsonResponse({ 'resp':'ok' })

def enviarDatos(request):
    cantidad = request.GET.get('cantidad')
    print(cantidad)
    ultimos_registros = estadoVehiculo.objects.all().order_by('-registroTiempo')[:int(cantidad)]
    arregloTiempos = []
    arregloInfos = []
    for reg in ultimos_registros:
        arregloTiempos.append(datetime.datetime.strftime(reg.registroTiempo,"%H:%M:%S"))
        arregloInfos.append(reg.registroInformacion)
    return JsonResponse({
        'informacionVehiculo':arregloInfos,
        'registroTiempos':arregloTiempos
    })

def descargarDatos(request):
    output = []
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    query_set = estadoVehiculo.objects.all().order_by('-registroTiempo')
    #Header
    writer.writerow(['Timestamp', 'Encendido'])
    for entry in query_set:
        timestamp = datetime.datetime.strftime(entry.registroTiempo,"%Y-%m-%dT%H:%M:%S")
        output.append([timestamp, entry.registroInformacion])
    #CSV Data
    writer.writerows(output)
    return response

