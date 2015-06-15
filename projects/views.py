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
            logger.debug(cntrm[0])
            logger.debug(checklist)
            if str(cntrm[0]) in checklist:
                checked = '1'
            else:
                checked = '0'
            np.checklist = np.checklist+cntr+" $# "+checked+" $$ "    
        if len(np.checklist)>1:
            np.checklist = np.checklist[:-4]
        np.attaches = request.POST['attaches']
        np.progress = request.POST['progress']
        np.status = request.POST['status']
        np.liables = request.POST.getlist('liables')
        np.observers = request.POST.getlist('observers')
        if request.POST['project']:
            np.project = Project.objects.filter(owner=request.user).filter(id=request.POST['project'])[0]
        else:
            np.project = curpr
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
    for cntr in range(len(flist)):
        chtrlst = flist[cntr].split(' $# ')
        catalog = catalog + chtrlst[0] + ' $# ' + chtrlst[1] + ' $$ '
        if chtrlst[2] == '1':
            checked = 'checked'
        else:
            checked = ''
        result = result+'<div><input type="checkbox" id="id_'+fname+'[]" name="'+fname+'[]" style="width:15px;" value='+chtrlst[0]+' '+checked+'>'+chtrlst[1]
        result = result+'&nbsp;&nbsp;&nbsp;<img src="/static/img/buttons/edit.png" onclick="editclelm(this,'+chtrlst[0]+');">'
        result = result+'&nbsp;<img src="/static/img/buttons/delete.png" onclick="deleteclelm(this,'+chtrlst[0]+');"></div>'
#           result = result+'<option value="'+chtrlst[0]+'" selected="selected">'+chtrlst[1]+'</option>'
#    result = result+'</select>'
    return {'chlist':result, 'catalog':catalog[:-4]}