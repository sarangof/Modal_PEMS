from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.create_pagina_empresas, name='create_form'),
]
