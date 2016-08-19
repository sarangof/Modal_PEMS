from __future__ import unicode_literals
from django.db import models

class Post(models.Model):
	file = models.FileField()
	sede = models.CharField(max_length=200)
	direccion = models.CharField(max_length=200)
	n_encuesta = models.IntegerField()
	

