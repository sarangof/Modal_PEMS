from django import forms
from .models import Datos_empresa, Cargar_encuesta

class FormForMyModel(forms.ModelForm):
	class Meta:
		model = Datos_empresa
		fields = "__all__"

class FormNuevaEmpresa(forms.ModelForm):
	class Meta:
		model = Datos_empresa
		fields = "__all__"

