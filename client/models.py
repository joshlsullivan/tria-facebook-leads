from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(max_length=254)
    cell_phone = models.CharField(max_length=(12), blank=True)
    company = models.CharField(max_length=120, blank=True)
    #Renamed from form_id to facebook_form_id
    facebook_form_id = models.CharField(max_length=120)
    has_mailchimp = models.BooleanField(default=False) #Mailchimp user
    mailchimp_dc = models.CharField(max_length=120, blank=True)
    mailchimp_list = models.CharField(max_length=120, blank=True)
    mailchimp_api = models.CharField(max_length=120, blank=True)
    has_drivecentric = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cell_phone
