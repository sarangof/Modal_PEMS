from __future__ import unicode_literals
from django.db import models

class Datos_empresa(models.Model):
	file1 = models.FileField()
	sede = models.CharField(max_length=200)
	direccion = models.CharField(max_length=200)
	n_encuesta = models.IntegerField()

OPCIONES_EMPRESA = (
    ('Buena Nota','BUENA NOTA'),
    ('TPTU', 'TPTU'),
)

class Cargar_encuesta(models.Model):
	empresa = models.FileField()
	
	

