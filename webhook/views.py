from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import NewLead
from client.models import Client
from django.contrib.auth.models import User
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.adobjects.lead import Lead
import json
import requests

app_id = '156847384730697'
app_secret = 'b62effe5ff8631745b15ce56ba38ea8b'
access_token = 'EAACOpuCmnEkBAAmZABKnaQPMWSaVu48SQv52sw3iW32iYCCI9komXVuobrhWjfPEvg3M0DmiKAKnU2WSzyaDQDIDAZCqihoQMDFcjRlahkDCl5TEddX1UGrYvfnvorh0vMJ2yF74ZAI3mtHN28t'
FacebookAdsApi.init(app_id, app_secret, access_token)

mg_api = 'key-640ad1685e02f6f088b805eaf2f1db66'

@xframe_options_exempt
def send_tagged_message(client_email, first_name, last_name, email, telephone, client_first_name, client_last_name):
    return requests.post(
        "https://api.mailgun.net/v3/mg.magnolia.technology/messages",
        auth=("api", mg_api),
        data={
            "from": "Josh Sullivan <josh@magnolia.technology>",
            "to": client_email,
            "subject": "New Lead - {0} {1}".format(first_name, last_name),
            "text": """Hi there, you have a new lead. Here's the info:
            First name: {0}
            Last name: {1}
            Email: {2}
            Telephone: {3}""".format(first_name, last_name, email, telephone),
            "o:tag": ["{0}-{1}".format(client_first_name, client_last_name).lower(), "facebook_leads"]
        }
    )

class WebhookView(generic.View):
    #Verifies the toke with Facebook app
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == access_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Wrong verify token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        incoming_lead = json.loads(self.request.body)
        lead_id = incoming_lead['entry'][0]['changes'][0]['value']['leadgen_id']
        lead = Lead(lead_id)
        fields=[
            Lead.Field.form_id, 
            Lead.Field.created_time,
            Lead.Field.id,
            Lead.Field.field_data,
            Lead.Field.ad_id,
        ]
        data = lead.remote_read(fields=fields)
        first_name = data['field_data'][0]['values'][0].encode('utf-8')
        last_name = data['field_data'][1]['values'][0].encode('utf-8')
        email = data['field_data'][2]['values'][0].encode('utf-8')
        telephone = data['field_data'][3]['values'][0].encode('utf-8')
        leadgen_id = str(data['id'])
        form_id = str(data['form_id'])
        ad_id = str(data['ad_id'])
        clients = User.objects.all()
        for client in clients:
            client_email = client.email
            client_first_name = client.first_name
            client_last_name = client.last_name
            if client.client.form_id == form_id:
                if data:
                    e = NewLead(first_name=first_name, last_name=last_name, email=email, telephone=telephone, form_id=form_id, leadgen_id=leadgen_id, ad_id=ad_id)
                    e.save()
                    def send_tagged_message(client_email=client_email, first_name=first_name, last_name=last_name, email=email, telephone=telephone, client_first_name=client_first_name, client_last_name=client_last_name)
        return HttpResponse()
