from __future__ import unicode_literals

from django.db import models
from client.models import Client

# Create your models here.

class Leads(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=120)
    form_id = models.CharField(max_length=120)
    leadgen_id = models.CharField(max_length=120)
    ad_id = models.CharField(max_length=120)
    date_created = models.DateTimeField(auto_now_add=True)
    has_contacted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Leads"

    def get_client(self):
        all_clients = Client.objects.all()
        for client in all_clients:
            if self.form_id == client.facebook_form_id:
                return "{0} {1}".format(client.first_name, client.last_name)

    def __str__(self):
        return self.email
