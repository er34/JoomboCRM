# -*- coding: utf-8 -*-

import datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import logging
from clients.views import GetNewCode, entry
from django.http import HttpResponse
from dela.forms import DelaEditForm
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from dela.models import Dela,Message
from JoomboCRM.settings import BASE_DIR
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage, send_mail
import smtplib

logger = logging.getLogger(__name__)

@csrf_protect
@login_required    
def settimeoffset(request):
    if request.method == 'POST':
        logger.debug(request.POST['usertime'])
        request.session['timeoffset'] = int(request.POST['usertime'])*60
        request.session['dateinput'] = request.POST['dateinput']
        logger.debug(request.session['timeoffset'])
        return entry(request)
    
def add(request, instance, folderclass):
    formname = _('NewDela')   
    timeoffsetstart = datetime.timedelta(0,request.session['timeoffset'])
    timeoffsetfinish = datetime.timedelta(0,request.session['timeoffset']-3600)
    delostart = datetime.datetime.utcnow()-timeoffsetstart
    delofinish = datetime.datetime.utcnow()-timeoffsetfinish
    form = DelaEditForm({'start': datetime.datetime.strftime(delostart, "%Y-%m-%dT%H:%M"),
                         'finish': datetime.datetime.strftime(delofinish, "%Y-%m-%dT%H:%M"),
                         'deladate': request.POST.get('deladate'),
                        })
    c = {'jeditform':form,
         'formname':formname,
         'modelname': 'Dela',
        }
    c.update(csrf(request))
    return render_to_response('editdela.html', c)
    
    
def copy(request, instance, folderclass):
    if instance.code:
        timeoffsetstart = datetime.timedelta(0,request.session['timeoffset'])
        timeoffsetfinish = datetime.timedelta(0,request.session['timeoffset']-3600)
        delostart = datetime.datetime.utcnow()-timeoffsetstart
        delofinish = datetime.datetime.utcnow()-timeoffsetfinish
        formname = _('CopyDela')
        form = DelaEditForm({'topic':instance.topic,
                             'start': datetime.datetime.strftime(delostart, "%Y-%m-%dT%H:%M"),
                             'finish': datetime.datetime.strftime(delofinish, "%Y-%m-%dT%H:%M"),
                             'content': instance.content,
                             'result': instance.result,
                             'deladate': request.POST.get('deladate'),
                            })
        c = {'jeditform':form,
             'formname':formname,
             'modelname': 'Dela',
            }
        c.update(csrf(request))
        return render_to_response('editdela.html', c)
    else:
        return None
        
def edit(request, instance, folderclass):
    if instance.code:
        timeoffset = datetime.timedelta(0, int(request.POST['timezome'])*60)
        if instance.start:
            start = datetime.datetime.strftime(instance.start-timeoffset, "%Y-%m-%dT%H:%M")
        else:
            start = None
        if instance.finish:
            finish = datetime.datetime.strftime(instance.finish-timeoffset, "%Y-%m-%dT%H:%M")
        else:
            finish = None
        if instance.finished:
            finished = datetime.datetime.strftime(instance.finished-timeoffset, "%Y-%m-%dT%H:%M")
        else:
            finished = None
        formname = _('EditingDela')
        form = DelaEditForm({'code': instance.code,
                             'topic':instance.topic,
                             'start': start,
                             'finish': finish,
                             'content': instance.content,
                             'result': instance.result,
                             'finished': finished,
                             'deladate': request.POST.get('deladate'),
                            })
        c = {'jeditform':form,
             'formname':formname,
             'modelname': 'Dela',
             'delo':instance,
            }
        c.update(csrf(request))
        return render_to_response('editdela.html', c)
    else:
        return None
        
def dblclick(request, instance, folderclass):
    return edit(request, instance, folderclass)
    
def enter(request, instance, folderclass):
    return edit(request, instance, folderclass)
    
def delete(request, instance, folderclass):
    if request.method == 'POST':
        instance.isdeleted = True
        deletemessages(instance)
        instance.save();
        return entry(request)
    
def editformprocessor(request):
    if request.POST['code']:
        nd = Dela.objects.filter(owner=request.user).filter(code=request.POST['code'])[0]
    else:
        nd = Dela(code=GetNewCode(Dela.objects.filter(owner_id = request.user.id)), owner = request.user)
    nd.topic = request.POST['topic']  
    if (request.POST['start']):
        nd.start = datetime.datetime.strptime(str(request.POST['start']), "%Y-%m-%dT%H:%M");
    if (request.POST['finish']):
        nd.finish = datetime.datetime.strptime(str(request.POST['finish']), "%Y-%m-%dT%H:%M");
    nd.content = request.POST['content'] 
    nd.result = request.POST['result']
    if (request.POST['finished']):
        nd.finished = datetime.datetime.strptime(str(request.POST['finished']), "%Y-%m-%dT%H:%M"); 
    if 'attache' in request.FILES:
        nd.attache = request.FILES['attache']
    addmessages(request, nd)
    nd.save()
    return entry(request)
    
def addmessages(request, nd):
    logger.debug(request.POST)
    if nd.finished == None:
        mf = False
        if 'sendstartsms' in request.POST and request.POST['sendstartsms']:
            messages = Message.objects.filter(owner=nd.owner).filter(topic=nd.topic).filter(sendtime=nd.start)
            if messages.count() == 0:
                mess = Message(owner=nd.owner)
                mess.topic = "Start task: "+nd.topic
                mess.content = nd.content
                mess.sendtime = nd.start
                mess.sendsms = True
                mess.sendmail = False
                mess.save()
                mf = True
        
        if 'sendstartmail' in request.POST and request.POST['sendstartmail']:
            if mf == False:
                messages = Message.objects.filter(owner=nd.owner).filter(topic=nd.topic).filter(sendtime=nd.start)
            if messages.count() == 0:
                mess = Message(owner=nd.owner)
                mess.topic = "Start task: "+nd.topic
                mess.content = nd.content
                mess.sendtime = nd.start
                mess.sendsms = False
                mess.sendmail = True
                mess.save()
                
        mf = False
        if 'sendfinishsms' in request.POST and request.POST['sendfinishsms']:
            messages = Message.objects.filter(owner=nd.owner).filter(topic=nd.topic).filter(sendtime=nd.finish)
            if messages.count() == 0:
                mess = Message(owner=nd.owner)
                mess.topic = unicode("End task: "+nd.topic)
                mess.content = unicode(nd.content).encode('utf-8')
                mess.sendtime = nd.finish
                mess.sendsms = True
                mess.sendmail = False
                mess.save()
                mf = True
        
        if 'sendfinishmail' in request.POST and request.POST['sendfinishmail']:
            if mf == False:
                messages = Message.objects.filter(owner=nd.owner).filter(topic=nd.topic).filter(sendtime=nd.finish)
            if messages.count() == 0:
                mess = Message(owner=nd.owner)
                mess.topic = unicode("End task: "+nd.topic)
                mess.content = unicode(nd.content).encode('utf-8')
                mess.sendtime = nd.finish
                mess.sendsms = False
                mess.sendmail = True
                mess.save()
                
def deletemessages(nd):
    messages = Message.objects.filter(owner=nd.owner).filter(topic=nd.topic).filter(sendtime=nd.start)
    for mess in messages:
        mess.delete()
        