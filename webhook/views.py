from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import NewLead
from client.models import Client
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.adobjects.lead import Lead
import json

app_id = '156847384730697'
app_secret = 'b62effe5ff8631745b15ce56ba38ea8b'
access_token = 'EAACOpuCmnEkBAAmZABKnaQPMWSaVu48SQv52sw3iW32iYCCI9komXVuobrhWjfPEvg3M0DmiKAKnU2WSzyaDQDIDAZCqihoQMDFcjRlahkDCl5TEddX1UGrYvfnvorh0vMJ2yF74ZAI3mtHN28t'
FacebookAdsApi.init(app_id, app_secret, access_token)

mg_api = 'key-640ad1685e02f6f088b805eaf2f1db66'

def send_tagged_message():
    return requests.post(
        "https://api.mailgun.net/v3/mg.magnolia.technology/messages",
        auth=("api", mg_api),
        data={"from": "Josh Sullivan <josh@magnolia.technology>",
              "to": client.email,
              "subject": "New Lead - {0} {1}".format(first_name, last_name),
              "text": """Hi there, you have a new lead. Here's the info:
              {0} {1}
              {2}
              {3}""".format(first_name, last_name, email, telephone),
              "o:tag": ["{0}{1}".format(client.first_name, client.last_name), "facebook_leads"]})

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
        incoming_lead = json.loads(self.request.body.decode('utf-8'))
        lead_id = incoming_lead['entry'][0]['changes'][0]['value']['leadgen_id']
        lead = Lead(lead_id)
        data = lead.remote_read()
        first_name = data['field_data'][0]['values']
        last_name = data['field_data'][1]['values']
        email = data['field_data'][2]['values']
        telephone = data['field_data'][3]['values']
        form_id = data['form_id']
        e = NewLead(first_name=first_name, last_name=last_name, email=email, telephone=telephone, form_id=form_id)
        e.save()
        #send_tagged_message()
        #print(created, form_id, first_name, last_name, email, telephone)
        return HttpResponse(data)
