from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import estadoTuberia
import datetime
import csv

# Create your views here.
def index(request):
    return render(request,"index.html")

def registrarDatos(request):
    datoMensaje = str(request.GET.get('mensaje'))
    datoTiempo = str(request.GET.get('tiempo'))
    print("Mensaje: ",datoMensaje,", tiempo:",datoTiempo)
    estadoTuberia(registroTiempo=datoTiempo,registroInformacion=datoMensaje).save()
    return JsonResponse({ 'resp':'ok' })

def enviarDatos(request):
    cantidad = request.GET.get('cantidad')
    ultimos_registros = estadoTuberia.objects.all().order_by('-registroTiempo')[:int(cantidad)]
    arregloTiempos = []
    arregloInfos = []
    for reg in ultimos_registros:
        arregloTiempos.append(datetime.datetime.strftime(reg.registroTiempo,"%Y-%m-%dT%H:%M:%S"))
        arregloInfos.append(reg.registroInformacion)
    return JsonResponse({
        'informacionTuberia':arregloInfos,
        'registroTiempos':arregloTiempos
    })

def descargarDatos(request):
    output = []
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    query_set = estadoTuberia.objects.all().order_by('-registroTiempo')
    #Header
    writer.writerow(['Timestamp', 'Caudal'])
    for entry in query_set:
        timestamp = datetime.datetime.strftime(entry.registroTiempo,"%Y-%m-%dT%H:%M:%S")
        output.append([timestamp, entry.registroInformacion])
    #CSV Data
    writer.writerows(output)
    return response

