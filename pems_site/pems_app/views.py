from django.shortcuts import render
from .forms import FormForMyModel, FormNuevaEmpresa

def create_form_parametros(request):
	form = FormForMyModel()
	context_data = {'form':form}
	return render(request,'pems_app/parametros_empresa.html', context_data)

def create_empresa(request):
	form = FormNuevaEmpresa()
	context_data = {'form':form}
	return render(request,'pems_app/cargar_empresa.html',context_data)

def create_pagina_empresas(request):
	return render(request,'pems_app/modulo_empresas.html')
