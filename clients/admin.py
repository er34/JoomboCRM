from django.contrib import admin
from clients.models import Client
from clients.models import Note

admin.site.register(Client)
admin.site.register(Note)