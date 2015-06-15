from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from contacts.forms import ContactEditForm
from clients.views import GetNewCode, entry
from clients.models import Client
from django.utils.translation import ugettext_lazy as _
from contacts.models import Contact
import datetime
import logging

logger = logging.getLogger(__name__)

def add(request, instance, folderclass):
    formname = _('NewContact')
    if 'clientid' in request.POST:
        form = ContactEditForm({'clientid':request.POST.get('clientid', None),})
        c = {'jeditform':form,
             'formname':formname,
             'modelname': 'Contact',
            }
        c.update(csrf(request))
        return render_to_response('editform.html', c)
        
def edit(request, instance, folderclass):
    if instance.code:
        if instance.birthday:
            birthday = datetime.datetime.strftime(instance.birthday, "%Y-%m-%d")
        else:
            birthday = '01.01.1880'    
        form = ContactEditForm({'code': instance.code,
                                'fio': instance.fio,
                                'phone': instance.phone,
                                'email': instance.email,
                                'birthday': birthday,
                                'position': instance.position,
                                'clientid': instance.client.code,
                                  })
        form.fields['clientid'].initial = instance.client.code
        formname = _('EditingContact')
        c = {'jeditform':form,
             'formname':formname,
             'modelname': 'Contact',
            }
        c.update(csrf(request))
        return render_to_response('editform.html', c)
    else:
        return None
 
def dblclick(request, instance, folderclass):
    return edit(request, instance, folderclass)
        
     
def enter(request, instance, folderclass):
    return edit(request, instance, folderclass)
    
def copy(request, instance, folderclass):
    if instance.code:
        formname = _('CopyContact')
        if instance.birthday:
            birthday = datetime.datetime.strftime(instance.birthday, "%Y-%m-%d")
        else:
            birthday = '01.01.1880'
        form = ContactEditForm({'fio': instance.fio,
                                'phone': instance.phone,
                                'email': instance.email,
                                'birthday': birthday,
                                'position': instance.position,
                                'clientid': instance.client.code,
                                      })
        c = {'jeditform':form,
             'formname':formname,
             'modelname': 'Contact',
            }
        c.update(csrf(request))
        return render_to_response('editform.html', c)
    else:
        return None
        
def delete(request, instance, folderclass):
    logger.debug(request.POST['clientid'])
    logger.debug(instance)
    if request.method == 'POST':
        instance.isdeleted = True
        instance.save();
        return entry(request)
     
def editformprocessor(request):
    logger.debug(request.POST['code'])
    if request.POST['code']:
        nc = Contact.objects.filter(owner=request.user).filter(code=request.POST['code'])[0]
    else:
        nc = Contact(code=GetNewCode(Contact.objects.filter(owner_id = request.user.id)), owner = request.user)
    nc.client = Client.objects.filter(owner_id = request.user.id).filter(code=request.POST['clientid'])[0]
    nc.fio = request.POST['fio']    
    nc.email = request.POST['email']  
    if (request.POST['birthday']):
        stdate = datetime.datetime.strptime(str(request.POST['birthday']), "%Y-%m-%d");
        nc.birthday = stdate    
    nc.position = request.POST['position']    
    nc.phone = request.POST['phone']    
    nc.save();
    return entry(request)