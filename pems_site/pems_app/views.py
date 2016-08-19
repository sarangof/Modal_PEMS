from django.shortcuts import render
from .models import Post
from .forms import FormForMyModel

def create_form(request):
	form = FormForMyModel()
	context_data = {'form':form}
	return render(request,'pems_app/template.html', context_data)
