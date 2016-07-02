from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from client.models import Client

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'
    
class UserAdmin(BaseUserAdmin):
    inlines = (ClientInline, )
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)