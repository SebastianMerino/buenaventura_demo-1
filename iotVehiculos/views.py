from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import subprocess
from .models import estadoVehiculo
import random
import csv

subprocess.Popen(["python3", "pruebaMQTT.py"])

# Create your views here.
def index(request):
    return render(request,"iotVehiculos/index.html")

def registrarDatos(request):
    datoMensaje = str(request.GET.get('mensaje'))
    datoTiempo = str(request.GET.get('tiempo'))
    if datoMensaje == 'N':
        datoMensaje = '0'
    elif datoMensaje == 'Y':
        datoMensaje = '1'
    if datoMensaje == '1' or datoMensaje == '0':
        estadoVehiculo(registroTiempo=str(request.GET.get('tiempo')),registroInformacion=datoMensaje).save()
    else:
        pass
    return JsonResponse({
        'resp':'ok'
    })

def enviarDatos(request):
    cantidad = request.GET.get('cantidad')
    print(cantidad)
    ultimos_registros = estadoVehiculo.objects.all().order_by('-id')[:int(cantidad)]
    arregloTiempos = []
    arregloInfos = []
    for reg in ultimos_registros:
        arregloTiempos.append(reg.registroTiempo.split('T')[1])
        arregloInfos.append(reg.registroInformacion)
    return JsonResponse({
        'informacionVehiculo':arregloInfos,
        'registroTiempos':arregloTiempos
    })

def descargarDatos(request):
    output = []
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    query_set = estadoVehiculo.objects.all()
    #Header
    writer.writerow(['Timestamp', 'Encendido'])
    for entry in query_set:
        output.append([entry.registroTiempo, entry.registroInformacion])
    #CSV Data
    writer.writerows(output)
    return response

