from django.db import models
from django.contrib.auth.models import User
    
class FriendsReltype(models.Model):
    name		= models.CharField(max_length=30, null=True, unique=False, blank=True)
    isdeleted 	= models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Friend(models.Model):
    user1 		= models.ForeignKey(User, null=False, blank=False, related_name='Friend_user1')
    user2 		= models.ForeignKey(User, null=False, blank=False, related_name='Friend_user2')
    Reltype 	= models.ForeignKey('FriendsReltype', null=False, blank=False, related_name='Note_user')
    
    def __unicode__(self):
        return self.user1.name + ' - ' + self.user2.name
        
class UserInfo(models.Model):
    owner 		= models.ForeignKey(User, null=False, blank=False, related_name='userinfo_owner')
    timezone    = models.IntegerField(null=True, unique=False, blank=True)
    phone       = models.CharField(max_length=20, null=True, unique=False, blank=True)
    
    def __unicode__(self):
        return self.owner.username