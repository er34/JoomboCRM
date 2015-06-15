from django.db import models
from django.contrib.auth.models import User
import datetime
from django_bleach.models import BleachField
  
class Message(models.Model):
    owner 		= models.ForeignKey(User, null=False, blank=False, related_name='messages_owner')
    topic 		= BleachField(max_length=100, null=False, unique=False, blank=False)
    content 	= models.TextField(null=True, unique=False, blank=True, default='')
    sendtime    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(1900,1,1,0,0))
    sendsms 	= models.BooleanField(default=False)
    sendmail 	= models.BooleanField(default=False)
    
    def __unicode__(self):
        return '(' + str(self.id) + ') ' + self.topic
        
class Dela(models.Model):
    owner 		= models.ForeignKey(User, null=False, blank=False, related_name='dela_owner')
    code 		= models.CharField(max_length=9, null=True, unique=False, blank=True)
    topic 		= BleachField(max_length=100, null=False, unique=False, blank=False)
    start	    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(1900,1,1,0,0))
    finish	    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(3000,1,1,0,0)) 
    content 	= models.TextField(null=True, unique=False, blank=True, default='')
    result   	= models.TextField(null=True, unique=False, blank=True, default='')
    finished    = models.DateTimeField(null=True, unique=False, blank=True) 
    attache     = models.FileField(upload_to='documents/%Y%m%d',null=True, blank=True)
    isdeleted 	= models.BooleanField(default=False)
    
    def __unicode__(self):
        return '(' + str(self.id) + ') ' + self.topic