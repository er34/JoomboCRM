from django.db import models

class Category(models.Model):
    code 		 = models.CharField(max_length=9, null=False, unique=True, blank=False)
    name         = models.CharField(max_length=255, null=False, unique=True, blank=False)
    isdeleted    = models.BooleanField(default=False)
    
class Reltype(models.Model):
    code 		= models.CharField(max_length=9, null=False, unique=True, blank=False)
    name         = models.CharField(max_length=255, null=False, unique=True, blank=False)
    isdeleted    = models.BooleanField(default=False)
    
class Region(models.Model):
    owner        = models.ForeignKey('clients.Client', null=False, blank=False, related_name='Region_owner')
    code 		= models.CharField(max_length=9, null=False, unique=True, blank=False)
    name         = models.CharField(max_length=255, null=False, unique=True, blank=False)
    isdeleted    = models.BooleanField(default=False)
