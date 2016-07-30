from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .models import Leads
from client.models import Client
from django.utils import timezone
import keen

def index(request):
    all_leads = Leads.objects.all()
    context = {
        'all_leads': all_leads,
    }
    return render(request, 'leads/index.html', context)

def get_leadgen_id():
    all_leads = Leads.objects.all()
    for lead in all_leads:
        return lead.leadgen_id

def detail(request, get_leadgen_id):
    newlead = get_object_or_404(NewLead, leadgen_id=get_leadgen_id)
    context = {
        'newlead': newlead,
    }
    return render(request, 'leads/detail.html', context)

def record_events(request):
    all_leads = Leads.objects.all()
    for lead in all_leads:
        keen.add_event("new_leads", {
            "name": "{0} {1}".format(lead.first_name, lead.last_name)
            "email": "{}".format(lead.email)
            "form id": '"{}"'.format(lead.form_id)
        })
        return lead
