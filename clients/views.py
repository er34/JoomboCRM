# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from clients.models import Client, Note
from contacts.models import Contact
from dela.models import Dela
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from clients.forms import ClientFolderEditForm, ClientEditForm
from django.utils.translation import ugettext as _
from operator import attrgetter
import logging
import datetime
from utils.Jdatatable.views import Jdatatable
from django.db.models import Q

logger = logging.getLogger(__name__)

class AuthForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# Main page
def entry(request, **kwargs):
#   logger.debug('debug message')
    if request.user.is_authenticated():
        if 'timeoffset' in request.session:
            timeoffset = datetime.timedelta(0,request.session['timeoffset'])
        else:
            timeoffset = datetime.timedelta(0,0)
        logger.debug(timeoffset)
        contacts = Contact.objects.all()
        contact_list = []
        daystart = datetime.datetime.combine(datetime.datetime.utcnow()-timeoffset, datetime.time(0))
        dayend = datetime.datetime.combine(datetime.datetime.utcnow()-timeoffset, datetime.time(23,59,59,99999))
        if timeoffset > datetime.timedelta(0,86400*730000):
            dela_list = list(Dela.objects.filter(owner=request.user).filter(isdeleted=False))
        else:
            dela_list = list(Dela.objects.filter(owner=request.user).filter(start__lte=dayend).filter(finish__gte=daystart).filter(isdeleted=False))
        dls = sorted(dela_list, key=attrgetter('start'), reverse=False)
        note = ''
        if 'parentcode' in kwargs:
            parentcode = kwargs['parentcode']
        elif 'parentcode' in request.POST:
            parentcode = request.POST['parentcode']
        elif 'parentcode' in request.session:
            parentcode = request.session['parentcode']
        else:
            parentcode = None
        request.session['parentcode'] = parentcode
        if parentcode:
            logger.debug(parentcode)
            folder = Client.objects.filter(owner=request.user).filter(code=parentcode)[0]
            clients_list = list(Client.objects.filter(parent=folder.id).filter(isdeleted=False).filter(owner=request.user))
            clients_list = [folder,]+clients_list
            while folder.parent:
                folder = folder.parent
                clients_list = [folder,]+clients_list
        elif request.method == 'POST':
            if 'clientid' in request.POST and request.POST['clientid'] and request.POST['clientid'] != '':
                cid = Client.objects.filter(owner=request.user).filter(code=request.POST['clientid'])[0].id
                note = Note.objects.filter(client_id=cid).filter(user_id=request.user.id).filter(isdeleted=False)
                contacts = Contact.objects.filter(client_id=cid).filter(isdeleted=False)
                contact_list = sorted(contacts, key=attrgetter('fio'), reverse=False)
                if len(note)>0:
                    note = note[0].content
                else:
                    note = ''
            clients_list = Client.objects.filter(parent__isnull=True).filter(isdeleted=False).filter(owner=request.user)
        else:
            clients_list = Client.objects.filter(parent__isnull=True).filter(isdeleted=False).filter(owner=request.user)
        cls = sorted(clients_list, key=attrgetter('code'), reverse=False)
        delacodes = ''
        if len(dls)>0:
            for cdc in dls:
                delacodes = delacodes+cdc.code+"," 
            delacodes = delacodes[:len(delacodes)-1] 
        cltable = Jdatatable(cls, ['code', 'name','uradress','phone',],
                             buttons = ['add', 'addfolder', 'copy', 'edit', 'delete'],
                             uid = 'Client_table',
                             parentcode = parentcode,)
        cntable = Jdatatable(contact_list, ['code', 'fio','phone','email','birthday','position',],
                             buttons = ['add', 'copy', 'edit', 'delete'],
                             uid = 'Contact_table',)
        delatablehead = '''<td rowspan=2 width="10px"></td>
                        <td width="80px">_start_</td><td rowspan=2>_topic_</td></tr>
						<tr class="datatablehead"><td>_finish_</td>'''
#        for dstr in dls:
#            dstr.start = datetime.datetime.strftime(dstr.start, "%H-%M")
        delatable = Jdatatable(dls, ['start', 'finish','topic',],
                             buttons = ['add', 'copy', 'delete', 'monthleft', 'left', 'right', 'monthright'],
                             uid = 'Dela_table',
                             tablehead = delatablehead,)
        if 'dateinput' in request.session:
            dateinput = request.session['dateinput']
        else:
            dateinput = ''
        c = {'parentcode': parentcode,
             'delacodes': delacodes,
             'note': note,
             'dela_list':dls,
             'cltable':cltable,
             'cntable':cntable,
             'delatable':delatable,
             'dateinput':dateinput,
             }
        c.update(csrf(request))
        return render_to_response('index.html', c)
    else:
        form = AuthForm()
        c = {'authform':form,
        }
        c.update(csrf(request))
        return render_to_response('login.html', c)
       
# login processor
@csrf_protect
def login(request):
#    f = open('C:\Bitnami\output.txt', 'a')
#    f.write('request.method')
#    f.close()
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        if request.method == 'POST':
            
            username = request.POST.get('login', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if (user is not None):
                if user.is_active:
                    auth.login(request, user)
        return HttpResponseRedirect(reverse('entry'))

def logout_view(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect("/")        
        
@login_required
@csrf_protect
def savenote(request):
    if request.method == 'POST' and 'value' in request.POST:
        cid = Client.objects.filter(owner=request.user).filter(code=request.POST.get('clientid'))[0].id
        note = Note.objects.filter(client_id=cid).filter(user_id=request.user.id).filter(isdeleted=False)
        if request.POST.get('value'):
            if len(note)>0:
                note = note[0]
            else:
                note = Note(client_id = cid, user_id = request.user.id, code = GetNewCode(Note.objects.filter(user_id = request.user.id)))
            note.content = request.POST.get('value')
            note.save()
        elif  len(note)>0:
            note = note[0]
            note.delete()
        return HttpResponse('success')

    

@csrf_protect    
def testrequest(request):
    if request.method == 'POST':
        arr = ['a','b'] 
        response_dict = {'note': 'test', 'arr': arr}
        return HttpResponse(response_dict)
    
#////////////////////////////// Helpers


# generates code for new object. arr - array of objects. Should have "code"!
def GetNewCode(arr):
    if len(arr)>0:
        cls = sorted(arr, key=attrgetter('code'), reverse=True)
        logger.debug(cls)
        lastcode = int(cls[0].code)
        logger.debug(lastcode)
        newcode = str(lastcode+1)
        while len(newcode)<9:
            newcode = '0'+newcode
        return newcode
    else:
        # first object
        return "000000001"
 
    def dblclick(self, tableid):
        return views.editclient(self, tableid)
        
    def enter(self):
        return self.dblclick()

def edit(request, instance, folderclass):
    if instance.code:
        if instance.parent:
            parentcode = instance.parent.code
        else:
            parentcode = ''
        if instance.isfolder:
            form = ClientFolderEditForm(instance=instance)
            formname = _('EditingClient')
        else:
            form = ClientEditForm(instance=instance)
            formname = _('EditingClient')
        c = {'jeditform':form,
             'formname':formname,
    #         'thisdialogid': request.POST['tableid'],
             'modelname': 'Client',
             'parentcode': parentcode,
            }
        c.update(csrf(request))
        return render_to_response('editform.html', c)
    else:
        return None
        
def dblclick(request, instance, folderclass):
    if instance.isfolder:
        if folderclass == "folderTrue folderTrueopened":
            if instance.parent:
                return entry(request, parentcode = instance.parent.code)
            else:
                return entry(request, parentcode = '')
        elif folderclass == "folderTrue folderTrueclosed":
            return entry(request, parentcode = instance.code)
        else:
            return entry(request)
    else:
        return edit(request, instance, folderclass)
        
     
def enter(request, instance, folderclass):
    return dblclick(request, instance, folderclass)
    
def add(request, instance, folderclass):
    formname = _('NewClient')
    if instance.parent:
        if folderclass == "folderTrue folderTrueopened":
            parent = Client.objects.filter(owner=request.user).filter(code=instance.code)[0]
        else:
            parent = Client.objects.filter(owner=request.user).filter(code=instance.parent.code)[0]
        logger.debug(parent)
        form = ClientEditForm({'parent': parent.id,}) 
        parentcode = instance.parent.code    
    else:
        form = ClientEditForm()
        parentcode = ''
    c = {'jeditform':form,
         'formname':formname,
         'modelname': 'Client',
         'parentcode': parentcode,
        }
    c.update(csrf(request))
    return render_to_response('editform.html', c)
    
def addfolder(request, instance, folderclass):
    formname = _('NewFolder')
    if instance.parent:
        if folderclass == "folderTrue folderTrueopened":
            parent = Client.objects.filter(owner=request.user).filter(code=instance.code)[0]
        else:
            parent = Client.objects.filter(owner=request.user).filter(code=instance.parent.code)[0]
        form = ClientFolderEditForm({'parent': parent.id,'isfolder': 'true',}) 
        parentcode = instance.parent.code    
    else:
        form = ClientFolderEditForm({'isfolder': 'true',})
        parentcode = ''
    c = {'jeditform':form,
         'formname':formname,
         'modelname': 'Client',
         'parentcode': parentcode,
        }
    c.update(csrf(request))
    return render_to_response('editform.html', c)
    
def copy(request, instance, folderclass):
    parentcode = ''
    formname = _('CopyClient')
    if instance.isfolder:
        if instance.parent:
            form = ClientFolderEditForm({'parent': instance.parent.id,
                                         'isfolder': 'true',
                                         'name': instance.name,
                                       })
            parentcode = instance.parent.code
        else:
            form = ClientFolderEditForm({'isfolder': 'true',
                                         'name': instance.name,
                                       })
    else:
        if instance.parent:
            form = ClientEditForm({'parent': instance.parent.id,
                                   'name': instance.name,
                                   'iscompany': instance.iscompany,
                                   'email': instance.email,
                                   'uradress': instance.uradress,
                                   'factadress': instance.factadress,
                                   'phone': instance.phone,
                                   'fax': instance.fax,
                                   'site': instance.site,
                                  })
            parentcode = instance.parent.code
        else:
            form = ClientEditForm({'name': instance.name,
                                   'iscompany': instance.iscompany,
                                   'email': instance.email,
                                   'uradress': instance.uradress,
                                   'factadress': instance.factadress,
                                   'phone': instance.phone,
                                   'fax': instance.fax,
                                   'site': instance.site,
                                  })
    c = {'jeditform':form,
         'formname':formname,
         'modelname': 'Client',
         'parentcode': parentcode,
        }
    c.update(csrf(request))
    return render_to_response('editform.html', c)
    
def delete(request, instance, folderclass):
    if xinstance.parent:
        parentcode = instance.parent.code
    else:
        parentcode = ''
    if request.method == 'POST':
        instance.isdeleted = True
        instance.save();
        logger.debug('delete'+instance.code)
        if instance.isfolder:
            chields = Client.objects.filter(parent=instance)
            for child in chields:
                delete(request, child, folderclass)
    if instance.code == request.POST['code']:
        return entry(request, parentcode = parentcode)
        
def editformprocessor(request):
    logger.debug(request.POST)
    if request.POST['code']:
        nc = Client.objects.filter(owner=request.user).filter(code=request.POST['code'])[0]
    else:
        nc = Client(code=GetNewCode(Client.objects.filter(owner_id = request.user.id)), owner = request.user)
#        nc.parent = Client.objects.filter(owner=request.user).filter(id=parcode)[0]
    if bool(request.POST['isfolder']):
        nc.name = request.POST['name'] 
        nc.isfolder = True
        if request.POST['parent']:
            nc.parent = Client.objects.get(id=request.POST['parent'])
        nc.save();
    else:
        if request.POST['parent']:
            nc.parent = Client.objects.get(id=request.POST['parent'])
        nc.isfolder = False
        nc.name = request.POST['name'] 
        nc.iscompany = request.POST.get('iscompany', True)
        nc.INN = request.POST['INN']    
        nc.KPP = request.POST['KPP']    
        nc.email = request.POST['email']    
        nc.uradress = request.POST['uradress']    
        nc.factadress = request.POST['factadress']    
        nc.phone = request.POST['phone']    
        nc.fax = request.POST['fax']    
        nc.site = request.POST['site']
        nc.save();
    return entry(request)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    