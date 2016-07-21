from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
#from django.views import generic
from django.views.generic import View
from client.models import Client
from leads.models import Leads
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
            "text": "Hi there, you have a new lead. Here's the info: \n First name: {0} \n Last name: {1} \n Email: {2} \n Telephone: {3} \n\n -Josh Sullivan".format(first_name, last_name, email, telephone),
            "o:tag": ["{0}-{1}".format(client_first_name, client_last_name).lower(), "facebook_leads"]
        }
    )

def subscribe_mailchimp(client_mailchimp_dc, client_mailchimp_list, client_mailchimp_api, first_name, last_name, email):
    #mailchim_dc referes to the mailchimp datacenter in api e.g. us5
    url = "https://" + client_mailchimp_dc + ".api.mailchimp.com/3.0/lists/" + client_mailchimp_list + "/members/"
    return requests.post(
        url,
        auth=('api', client_mailchimp_api),
        data={
            "email_address":email,
            "status":"pending",
            "merge_fields":{
                "FNAME":first_name,
                "LNAME":last_name,
            }
        }
    )

def get_values(data, name):
    for data_element in data.get('field_data'):
        if data_element.get('name') == name:
            return data_element.get('values')
    return None

class WebhookView(View):
    #Verifies the toke with Facebook app
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == access_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Wrong verify token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        #return generic.View.dispatch(self, request, *args, **kwargs)
        return super(WebhookView, self).dispatch(request, *args, **kwargs)

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
        first_name = get_values(data, 'first_name')[0]
        last_name = get_values(data, 'last_name')[0]
        email = get_values(data, 'email')[0]
        telephone = get_values(data, 'phone_number')[0]
        leadgen_id = str(data['id'])
        form_id = str(data['form_id'])
        ad_id = str(data['ad_id'])
        clients = User.objects.all()
        for c in clients:
            if data:
                client_email = c.email
                client_first_name = c.first_name
                client_last_name = c.last_name
                client_mailchimp_dc = c.client.mailchimp_dc
                client_mailchimp_list = c.client.mailchimp_list
                client_mailchimp_api = c.client.mailchimp_api
                e = Leads(first_name=first_name, last_name=last_name, email=email, telephone=telephone, form_id=form_id, leadgen_id=leadgen_id, ad_id=ad_id)
                e.save()
                if c.client.facebook_form_id == form_id:
                    send_tagged_message(client_email=client_email, first_name=first_name, last_name=last_name, email=email, telephone=telephone, client_first_name=client_first_name, client_last_name=client_last_name)
                    if c.client.has_mailchimp == True:
                        subscribe_mailchimp(client_mailchimp_dc=client_mailchimp_dc, client_mailchimp_list=client_mailchimp_list, client_mailchimp_api=client_mailchimp_api, first_name=first_name, last_name=last_name, email=email)
        return HttpResponse()
