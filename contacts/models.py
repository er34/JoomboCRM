from django.db import models
from clients.models import Client
from django.contrib.auth.models import User
from django_bleach.models import BleachField

class Contact(models.Model):
    code 		= models.CharField(max_length=9, null=False, unique=False, blank=False)
    client 		= models.ForeignKey(Client, null=False, blank=False, related_name='contact_client')
    fio 		= BleachField(max_length=255, null=False, unique=False, blank=False)
    email 		= BleachField()
    birthday	= models.DateField(null=True, unique=False, blank=True)
    position	= BleachField(max_length=150, null=True, unique=False, blank=True)
    phone		= BleachField(max_length=30, null=True, unique=False, blank=True)
    isdeleted 	= models.BooleanField(default=False)
    owner 	    = models.ForeignKey(User, null=True, blank=True, related_name='contact_owner')

    def __unicode__(self):
        return '(' + str(self.id) + ') ' + self.fio
