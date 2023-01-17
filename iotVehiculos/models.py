from django.db import models

# Create your models here.
class estadoVehiculo(models.Model):
    registroTiempo = models.CharField(max_length=32,default="")
    registroInformacion = models.CharField(max_length=16,default="")