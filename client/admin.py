from django.contrib import admin
from client.models import Client

class ClientAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'email',
        'cell_phone',
        'company',
        'facebook_form_id',
        'has_mailchimp',
        'mailchimp_dc',
        'mailchimp_list',
        'mailchimp_api',
        'has_drivecentric',
    )
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('date_added', )

admin.site.register(Client, ClientAdmin)
