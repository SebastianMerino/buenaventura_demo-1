from django.db import models

# Create your models here.
class estadoTuberia(models.Model):
    registroTiempo = models.DateTimeField()
    registroInformacion = models.FloatField()