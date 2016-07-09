from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Leads(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254, unique=True)
    telephone = models.CharField(max_length=120)
    form_id = models.CharField(max_length=120)
    leadgen_id = models.CharField(max_length=120)
    ad_id = models.CharField(max_length=120)
    date_created = models.DateTimeField(auto_now_add=True)
    has_contacted = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = "Leads"
    
    def get_leads(self):
        all_leads = Leads.objects.all()
        for leads in all_leads:
            return leads.form_id
        
    def client(self):
        all_clients = User.objects.all()
        for client in all_clients:
            if client.client.form_id == get_leads():
                return ("%s %s" % (client.first_name, client.last_name))
            
    def __str__(self):
        return self.email