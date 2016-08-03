from django.contrib import admin
from client.models import Client

class ClientAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'email',
        'cell_phone',
        'company',
        'facebook_page_id',
        'facebook_form_id',
        'has_mailchimp',
        'mailchimp_dc',
        'mailchimp_list',
        'mailchimp_api',
        'has_adf_crm',
        'adf_email',
    )
    list_display = ('first_name', 'last_name', 'email', 'company')
    list_filter = ('date_added', )

admin.site.register(Client, ClientAdmin)
