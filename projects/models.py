from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django_bleach.models import BleachField

class Project(models.Model):
    code 		= models.CharField(max_length=9, null=False, unique=False, blank=False, verbose_name = _('Code'))
    owner 		= models.ForeignKey(User, null=False, blank=False, related_name='project_owner')
    admins      = models.ManyToManyField(User, related_name='project_admins',)
    members     = models.ManyToManyField(User, related_name='project_members',)
    start	    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(1900,1,1,0,0))
    finish	    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(3000,1,1,0,0))
    changedate  = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime.utcnow())
    createdate  = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime.utcnow())
    topic 		= BleachField(max_length=100, null=False, unique=False, blank=False)
    content 	= models.TextField(null=True, unique=False, blank=True, default='')
    progress    = models.IntegerField(null=True, unique=False, blank=True)
    isdeleted 	= models.BooleanField(default=False)
    
    def __unicode__(self):
        return '(' + str(self.id) + ')'+ self.code + ' ' + self.topic
    
class Task(models.Model):
    code 		= models.CharField(max_length=9, null=False, unique=False, blank=False, verbose_name = _('Code'))
    owner 		= models.ForeignKey(User, null=False, blank=False, related_name='task_owner')
    project 	= models.ForeignKey(Project, null=False, blank=False, related_name='task_project')
    parent      = models.ForeignKey('self', null=True, blank=True, related_name='task_parent', verbose_name=_('Parent'))
    liable 		= models.ForeignKey(User, null=False, blank=False, related_name='task_liable')
    admins      = models.ManyToManyField(User, related_name='task_admins',)
    liables     = models.ManyToManyField(User, related_name='task_liables',)
    observers   = models.ManyToManyField(User, related_name='task_observers',)
    start	    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(1900,1,1,0,0))
    finish	    = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime(3000,1,1,0,0))
    changedate  = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime.utcnow())
    createdate  = models.DateTimeField(null=True, unique=False, blank=True, default=datetime.datetime.utcnow())
    topic 		= BleachField(max_length=100, null=False, unique=False, blank=False)
    content 	= models.TextField(null=True, unique=False, blank=True, default='')
    progress    = models.IntegerField(null=True, unique=False, blank=True)
    status 		= models.CharField(max_length=20, null=False, unique=False, blank=False, verbose_name = _('Status'))
    statushist 	= models.TextField(null=True, unique=False, blank=True, default='')
    result 	    = models.TextField(null=True, unique=False, blank=True, default='')
    finished    = models.DateTimeField(null=True, unique=False, blank=True)
    checklist 	= models.TextField(null=True, unique=False, blank=True, default='')
    attaches    = models.TextField(null=True, unique=False, blank=True, default='')
    isdeleted 	= models.BooleanField(default=False)
    
    def __unicode__(self):
        return '(' + str(self.id) + ')'+ self.code + ' ' + self.topic