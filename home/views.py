from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"

class DeleteAppView(TemplateView):
    template_name = "delete.html"
