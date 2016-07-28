from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
#from django.views import generic
from django.views.generic import View
from client.models import Client
from leads.models import Leads
#from django.contrib.auth.models import User
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.adobjects.lead import Lead
import json
import requests

FacebookAdsApi.init(settings.APP_ID, settings.APP_SECRET, settings.ACCESS_TOKEN)

@xframe_options_exempt
def send_tagged_message(client_email, first_name, last_name, email, telephone, client_first_name, client_last_name):
    return requests.post(
        "https://api.mailgun.net/v3/mg.magnolia.technology/messages",
        auth=("api", settings.MG_API),
        data={
            "from": "Josh Sullivan <josh@magnolia.technology>",
            "to": client_email,
            "subject": "New Lead - {0} {1}".format(first_name, last_name),
            "text": "Hi there, you have a new lead. Here's the info: \n First name: {0} \n Last name: {1} \n Email: {2} \n Telephone: {3} \n\n -Josh Sullivan".format(first_name, last_name, email, telephone),
            "o:tag": ["{0}-{1}".format(client_first_name, client_last_name).lower(), "facebook_leads"],
        }
    )

@xframe_options_exempt
def send_drivecentric_email(client_drivecentric_email, client_email, first_name, last_name, time_of_lead, telephone, email, client_first_name, client_last_name):
    business_name = "Magnolia Tech Facebook"
    return requests.post(
        "https://api.mailgun.net/v3/mg.magnolia.technology/messages",
        auth=("api", settings.MG_API),
        data={
            "from": "Josh Sullivan <josh@magnolia.technology>",
            "to": client_drivecentric_email,
            "cc": client_email,
            "subject": "New Lead - {0} {1}".format(first_name, last_name),
            "text":'<?xml version="1.0" encoding="UTF-8"?><?adf version="1.0"?><adf><prospect><requestdate>' + time_of_lead + '</requestdate><customer><contact><name part="first">' + first_name + '</name><name part="last">' + last_name + '</name><phone>' + telephone + '</phone><email>' + email + '</email></contact></customer><vendor><contact><name part="full">' + business_name + '</name></contact></vendor></prospect></adf>',
            "o:tag": ["{0}-{1}".format(client_first_name, client_last_name).lower(), "facebook_leads_drivecentric"],
        }
    )

def subscribe_mailchimp(client_mailchimp_dc, client_mailchimp_list, client_mailchimp_api, first_name, last_name, email):
    #mailchim_dc referes to the mailchimp datacenter in api e.g. us5
    return requests.post(
        "https://" + client_mailchimp_dc + ".api.mailchimp.com/3.0/lists/" + client_mailchimp_list + "/members/",
        auth=('api', client_mailchimp_api),
        data={
            "email_address": email,
            "status": "pending",
            "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name
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
        time_of_lead = str(data['created_time'])
        leadgen_id = str(data['id'])
        form_id = str(data['form_id'])
        ad_id = str(data['ad_id'])
        clients = Client.objects.all()
        for client in clients:
            if client.facebook_form_id == form_id:
                client_email = client.email
                client_first_name = client.first_name
                client_last_name = client.last_name
                client_mailchimp_dc = client.mailchimp_dc
                client_mailchimp_list = client.mailchimp_list
                client_mailchimp_api = client.mailchimp_api
                client_drivecentric_email = client.drivecentric_email
                e = Leads(first_name=first_name, last_name=last_name, email=email, telephone=telephone, form_id=form_id, leadgen_id=leadgen_id, ad_id=ad_id)
                e.save()
                if client.has_drivecentric:
                    send_drivecentric_email(client_drivecentric_email=client_drivecentric_email, time_of_lead=time_of_lead, client_email=client_email, first_name=first_name, last_name=last_name, email=email, telephone=telephone, client_first_name=client_first_name, client_last_name=client_last_name)
                else:
                    send_tagged_message(client_email=client_email, first_name=first_name, last_name=last_name, email=email, telephone=telephone, client_first_name=client_first_name, client_last_name=client_last_name)
            else:
                print("Your not a client in our database.")
        return HttpResponse()
