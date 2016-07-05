from django.contrib import admin
from .models import Leads

class NewLeadAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'telephone', 'leadgen_id', 'form_id', 'ad_id']
    
admin.site.register(Leads, NewLeadAdmin)