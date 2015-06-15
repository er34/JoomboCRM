from django.contrib import admin
from multiuser.models import Friend, FriendsReltype, UserInfo

admin.site.register(Friend)
admin.site.register(FriendsReltype)
admin.site.register(UserInfo)