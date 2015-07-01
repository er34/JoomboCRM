# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from clients.views import AuthForm
from projects.models import Project, Task
from projects.forms import ProjectEditForm, TaskEditForm
from utils.Jdatatable.views import Jdatatable
from operator import attrgetter
from django.utils.translation import ugettext_lazy as _
import datetime
from clients.views import GetNewCode
from django.contrib.auth.models import User
import JoomboCRM.settings as settings
import os

import logging
logger = logging.getLogger(__name__)

def projectsentry(request, **kwargs):
    tls = [] # задачи
    projects_list = Project.objects.filter(isdeleted=False).filter(owner=request.user)
    pls = sorted(projects_list, key=attrgetter('start'), reverse=False)
    projectscodes = ''
    if len(pls)>0:
        for cdc in pls:
            projectscodes = projectscodes+cdc.code+"," 
        projectscodes = projectscodes[:len(projectscodes)-1]
    if 'projectid' in request.POST and request.POST['projectid'] and request.POST['projectid'] != '':
        pjct = Project.objects.filter(owner=request.user).filter(code=request.POST['projectid'])[0].id
        task_list = list(Task.objects.filter(project_id=pjct).filter(isdeleted=False).filter(owner=request.user))
        tls = sorted(task_list, key=attrgetter('code'), reverse=False)
    tasktable = Jdatatable(tls, ['code', 'topic','start','finish','owner','liable','progress',],
                             buttons = ['add', 'copy', 'edit', 'delete'],
                             uid = 'Task_table',)
    if request.user.is_authenticated():
        c = {'projectcodes':projectscodes,
             'project_list':pls,
             'tasktable':tasktable,}
        c.update(csrf(request))
        return render_to_response('projects.html', c)
    else:
        form = AuthForm()
        c = {'authform':form,
        }
        c.update(csrf(request))
        return render_to_response('login.html', c)

def add(request, instance, folderclass):
    formname = _('NewProject')   
    startoffset = datetime.timedelta(0, int(request.POST['timezome'])*60)
    finishoffset = datetime.timedelta(0, int(request.POST['timezome'])*60-86400)
    start = datetime.datetime.strftime(datetime.datetime.utcnow()-startoffset, "%Y-%m-%dT%H:%M")
    finish = datetime.datetime.strftime(datetime.datetime.utcnow()-finishoffset, "%Y-%m-%dT%H:%M")
    form = ProjectEditForm({'start': start,
                         'finish': finish,
                         'deladate': request.POST.get('deladate'),
                        })
    c = {'jeditform':form,
         'formname':formname,
         'modelname': 'Project',
        }
    c.update(csrf(request))
    return render_to_response('editform.html', c)
    
def copy(request, instance, folderclass):
    if instance.code:
        formname = _('CopyProject')
        startoffset = datetime.timedelta(0, int(request.POST['timezome'])*60)
        finishoffset = datetime.timedelta(0, int(request.POST['timezome'])*60-86400)
        start = datetime.datetime.strftime(datetime.datetime.utcnow()-startoffset, "%Y-%m-%dT%H:%M")
        finish = datetime.datetime.strftime(datetime.datetime.utcnow()-finishoffset, "%Y-%m-%dT%H:%M")
        
        form = ProjectEditForm({'topic':instance.topic,
                             'start': start,
                             'finish': finish,
                             'content': instance.content,
                             'admins': instance.admins.all(),
                             'members': instance.members.all(),
                            })
        c = {'jeditform':form,
             'formname':formname,
             'modelname': 'Project',
            }
        c.update(csrf(request))
        return render_to_response('editform.html', c)
    else:
        return None
        
def edit(request, instance, folderclass):
    logger.debug
    if instance.code:
        formname = _('EditingProject')
        timeoffset = datetime.timedelta(0, int(request.POST['timezome'])*60)
        if instance.start:
            start = datetime.datetime.strftime(instance.start-timeoffset, "%Y-%m-%dT%H:%M")
        else:
            start = None
        if instance.finish:
            finish = datetime.datetime.strftime(instance.finish-timeoffset, "%Y-%m-%dT%H:%M")
        else:
            finish = None
        if instance._meta.model == Project:
            formname = _('EditingProject')
            form = ProjectEditForm({'code': instance.code,
                                 'topic':instance.topic,
                                 'start': start,
                                 'finish': finish,
                                 'content': instance.content,
                                 'admins': instance.admins.all(),
                                 'members': instance.members.all(),                                   
                                })
            c = {'jeditform':form,
                 'formname':formname,
                 'modelname': 'Project',
                }
            c.update(csrf(request))
            return render_to_response('editform.html', c)
        elif instance._meta.model == Task:
            formname = _('EditingTask')
            checklist = getchecklist(instance.checklist, 'checklist')
            attachestab = getattaches(instance.attaches, 'attaches')
            attaches = {'tab':attachestab, 'catalog':instance.attaches}
            if instance.finished:
                finished = datetime.datetime.strftime(instance.finished-timeoffset, "%Y-%m-%dT%H:%M")
            else:
                finished = None
            form = TaskEditForm({'code': instance.code,
                                 'project':instance.project,
                                 'parent':instance.parent,
                                 'liable':instance.liable,
                                 'topic':instance.topic,
                                 'start': start,
                                 'finish': finish,
                                 'content': instance.content,
                                 'finished': finished,
                                 'result':instance.result,
                                 'checklist':instance.checklist,
                                 'attaches':instance.attaches,
                                 'progress':instance.progress,
                                 'status':instance.status,
                                 'statushist':instance.statushist,
                                 'admins': instance.admins.all(),
                                 'liables': instance.liables.all(),
                                 'observers': instance.observers.all(),
                                 'projectid': instance.project.code,
                                })
            c = {'jeditform':form,
                 'formname':formname,
                 'modelname': 'Task',
                 'checklist': checklist,
                 'attaches':attaches,
                }
            c.update(csrf(request))
            return render_to_response('edittask.html', c)
    else:
        return None
        
def dblclick(request, instance, folderclass):
    return edit(request, instance, folderclass)
    
def enter(request, instance, folderclass):
    return edit(request, instance, folderclass)
    
def editformprocessor(request):
    logger.debug(request)
    if 'liable' in request.POST:    # это задачи
        if request.POST['code']:
            np = Task.objects.filter(owner=request.user).filter(code=request.POST['code'])[0]
        else:
            np = Task(code=GetNewCode(Task.objects.filter(owner_id = request.user.id)), owner = request.user, progress = 0)
        curpr = Project.objects.filter(owner=request.user).filter(code=request.POST['projectid'])[0]
        if request.POST['parent']:
            np.parent = Task.objects.filter(owner=request.user).filter(id=request.POST['parent'])[0]
        else: 
            np.parent = None
        if request.POST['liable']:
            np.liable = User.objects.get(id=request.POST['liable'])
        if (request.POST['finished']):
            np.finished = datetime.datetime.strptime(str(request.POST['finished']), "%Y-%m-%dT%H:%M");
        np.result = request.POST['result']
        checkcatalog = request.POST['checkcatalog'].split(' $$ ')
        checklist = request.POST.getlist('checklist[]')
        np.checklist = ''
        for cntr in checkcatalog:
            cntrm = cntr.split(' $# ')
            if str(cntrm[0]) in checklist:
                checked = '1'
            else:
                checked = '0'
            np.checklist = np.checklist+cntr+" $# "+checked+" $$ "    
        if len(np.checklist)>1:
            np.checklist = np.checklist[:-4]
        np.progress = request.POST['progress']
        np.status = request.POST['status']
        np.liables = request.POST.getlist('liables')
        np.observers = request.POST.getlist('observers')
        if request.POST['project']:
            np.project = Project.objects.filter(owner=request.user).filter(id=request.POST['project'])[0]
        else:
            np.project = curpr
        flist = request.FILES.getlist('attaches')
        
# delete old files
        oldfiles = np.attaches.split('; ')
        attcatalog = request.POST['attcatalog']
        for fl in oldfiles:
            if attcatalog.find(fl)<0:
                os.remove(fl.replace(settings.MEDIA_URL, settings.MEDIA_ROOT))
        np.attaches = attcatalog
        
# add new files
        if len(flist)>0:
            fway = settings.MEDIA_ROOT+'documents/'+datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")+'/'
            fhref =  settings.MEDIA_URL+'documents/'+datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")+'/'
            if not os.path.exists(fway):
                os.makedirs(fway)
            for fl in flist:
                fdname = fway+fl.name
                fname = fhref+fl.name
                nfl = open(fdname, 'wb+')
                for chunk in fl.chunks():
                    nfl.write(chunk)
                nfl.close()
                np.attaches = np.attaches+fname+'; '
    else:
        if request.POST['code']:
            np = Project.objects.filter(owner=request.user).filter(code=request.POST['code'])[0]
        else:
            np = Project(code=GetNewCode(Project.objects.filter(owner_id = request.user.id)), owner = request.user, progress = 0)  
        np.members = request.POST.getlist('members')
    if (request.POST['start']):
        np.start = datetime.datetime.strptime(str(request.POST['start']), "%Y-%m-%dT%H:%M");
    if (request.POST['finish']):
        np.finish = datetime.datetime.strptime(str(request.POST['finish']), "%Y-%m-%dT%H:%M");
    np.content = request.POST['content'] 
    np.admins = request.POST.getlist('admins')
    np.topic = request.POST['topic']
    np.save()
    return projectsentry(request)
    
def delete(request, instance, folderclass):
    if request.method == 'POST':
        instance.isdeleted = True
        instance.save();
        return projectsentry(request)
        
def getchecklist(field, fname):
#    result =  '<select multiple="multiple" id="id_'+fname+'" name="'+fname+'">'
#    result = '<div style="width: 100%;height: 100px;overflow: scroll;background-color: white;border: 1px solid #aaaaaa;">'
    catalog = ''
    result = ''
    flist = field.split(' $$ ')
    result = result + '<table class="checklist" id="cltable" width="100%">'
    for cntr in range(len(flist)):
        chtrlst = flist[cntr].split(' $# ')
        catalog = catalog + chtrlst[0] + ' $# ' + chtrlst[1] + ' $$ '
        logger.debug(chtrlst[1])
        if chtrlst[2] == '1':
            checked = 'checked'
        else:
            checked = ''
        result = result+'<tr><td><input type="checkbox" id="id_'+fname+'[]" name="'+fname+'[]" style="width:15px;" value='+chtrlst[0]+' '+checked+'></td>'
        result = result+'<td><span style="cursor:pointer" onclick="editclelm(this,'+chtrlst[0]+');">'+chtrlst[1]+'</span></td>'
        result = result+'<td><img src="/static/img/buttons/delete.png" style="cursor:pointer" onclick="deleteclelm(this,'+chtrlst[0]+');"></td></tr>'
    addclcnst = _('Add')
    result = result + '<tr id="addclelmtr"><td style="text-align:center;cursor:pointer;" colspan=3 onclick="addclelm() ">'+addclcnst.translate('ru')+'</td></tr></table>'
#           result = result+'<option value="'+chtrlst[0]+'" selected="selected">'+chtrlst[1]+'</option>'
#    result = result+'</select>'
    return {'chlist':result, 'catalog':catalog[:-4]}
    
def getattaches(field, fname):
    if len(field)>0:
        result = '<table width="100%">'
        flist = field.split('; ');
        flist.remove(flist[-1])
        for fl in flist:
            sfl = os.path.split(fl)
            result = result + '<tr id="'+fl+'"><td><a href="'+fl+'">'+sfl[1]+'</a></td>'
            result = result + '<td width="20px"><img src="/static/img/buttons/delete.png" style="cursor:pointer" onclick="deletefl(this);"></td></tr>'
        result = result + '</table>'
        return result
    