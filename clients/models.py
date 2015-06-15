from django.db import models
from django.contrib.auth.models import User
from jdirs.models import Category, Reltype, Region
from django.utils.translation import ugettext_lazy as _
from django_bleach.models import BleachField

from django.shortcuts import render_to_response
from django.core.context_processors import csrf

class Client(models.Model):
    owner 		= models.ForeignKey(User, null=False, blank=False, related_name='client_owner')
    parent      = models.ForeignKey('self', null=True, blank=True, related_name='client_parent', verbose_name=_('Parent'))
    isfolder 	= models.BooleanField(default=False)
    code 		= models.CharField(max_length=9, null=False, unique=False, blank=False, verbose_name = _('Code'))
    name 		= BleachField(max_length=255, null=True, unique=False, blank=True, verbose_name = _('Name'))
    iscompany 	= models.BooleanField(default=True)
    INN 		= models.CharField(max_length=12, null=True, unique=False, blank=True)
    KPP 		= models.CharField(max_length=12, null=True, unique=False, blank=True)
    email 		= models.EmailField()
    uradress	= BleachField(max_length=150, null=True, unique=False, blank=True,  verbose_name = _('Uradress'))
    factadress	= models.CharField(max_length=150, null=True, unique=False, blank=True, verbose_name = _('Factadress'))
    phone		= BleachField(max_length=30, null=True, unique=False, blank=True, verbose_name = _('Phone'))
    fax			= models.CharField(max_length=30, null=True, unique=False, blank=True)
    site		= models.CharField(max_length=50, null=True, unique=False, blank=True)
    isdeleted 	= models.BooleanField(default=False)
    region 		= models.ForeignKey(Region, null=True, blank=True, related_name='client_region')
    categoty	= models.ForeignKey(Category, null=True, blank=True, related_name='client_category')
    reltype		= models.ForeignKey(Reltype, null=True, blank=True, related_name='client_reltype')
    
    def __unicode__(self):
        return '(' + str(self.id) + ')'+ self.code + ' ' + self.name

        
class Note(models.Model):
    code 		= models.CharField(max_length=9, null=False, unique=False, blank=False)
    client 		= models.ForeignKey(Client, null=False, blank=False, related_name='Note_client')
    content 	= models.TextField(null=True, unique=False, blank=True, default='')
    isdeleted 	= models.BooleanField(default=False)
    user 		= models.ForeignKey(User, null=False, blank=False, related_name='Note_user')

    def __unicode__(self):
        if len(self.content) > 25:
            cont = '...'
        else:
            cont = ''
        return self.client.code + ' ' + self.client.name + '   ' + self.content[:25] + cont
        