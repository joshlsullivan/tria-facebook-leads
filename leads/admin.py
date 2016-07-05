from django.db import models
from django.contrib import admin
from .models import Leads

class NewLeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'telephone', 'client')
    list_filter = ('date_created', 'has_contacted')
    
admin.site.register(Leads, NewLeadAdmin)