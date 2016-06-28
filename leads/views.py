from django.shortcuts import render
from webhook.models import NewLead
from client.models import Client

# Create your views here.
def get_leads(request):
    clients = Client.objects.all()
    latest_leads = NewLead.objects.order_by('-date_created')[:5]
    context = {'latest_leads': latest_leads}
    return render(request, 'client/index.html', context)