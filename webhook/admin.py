from django.contrib import admin
from .models import NewLead

class NewLeadAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'telephone']
    
admin.site.register(NewLead, NewLeadAdmin)