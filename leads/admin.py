from django.db import models
from django.contrib import admin
from .models import Leads

class NewLeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'telephone', 'get_client')
    list_filter = ('date_created', 'has_contacted')
    list_per_page = 20

admin.site.register(Leads, NewLeadAdmin)
