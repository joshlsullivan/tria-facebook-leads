from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cell_phone = models.CharField(max_length=(12), blank=True)
    company = models.CharField(max_length=120, blank=True)
    form_id = models.CharField(max_length=120, blank=True)
    
    def __str__(self):
        return self.cell_phone