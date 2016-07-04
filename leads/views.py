from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from webhook.models import NewLead
from client.models import Client
from django.utils import timezone

def index(request):
    all_leads = NewLead.objects.all()
    context = {
        'all_leads': all_leads,
    }
    return render(request, 'leads/index.html', context)

def get_leadgen_id():
    all_leads = NewLead.objects.all()
    for lead in all_leads:
        return lead.leadgen_id

def detail(request, get_leadgen_id):
    newlead = get_object_or_404(NewLead, leadgen_id=get_leadgen_id)
    context = {
        'newlead': newlead,
    }
    return render(request, 'leads/detail.html', context)

