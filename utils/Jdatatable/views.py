# -*- coding: utf-8 -*-

# possible kwargs: 
# buttons = ['add', 'addfolder', 'copy', 'edit', 'delete'] 
# parentcode = '' (code of current parent folder)

from __future__ import unicode_literals
import logging
import uuid
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.loading import get_model
import JoomboCRM.settings as settings
from django.utils.module_loading import import_module


logger = logging.getLogger('utils.Jdatatable')

# 1 queryset, 2 list of columns
def Jdatatable(dataset, columns=[], **kwargs):
    logger.debug(dataset)
    if 'uid' in kwargs:
        uid = kwargs['uid']
        model = jgetmodel(uid[:uid.find('_')])['model']
    else:
        if dataset.__class__.__name__ == 'list':
            uid = dataset[0].__class__.__name__
            model = dataset[0].__class__
        elif dataset.__class__.__name__ == 'QuerySet':
            uid = dataset.model.__name__
            model = dataset.model
        else:
            return 'wrong dataset fir Jdatatable'
        if 'id' in kwargs:
            uid = uid + '_' + kwargs['id']
        else:
            udi = uid+'_'+str(uuid.uuid4()).replace("-","")
    if len(columns)>0:
        if 'tablehead' in kwargs:
            datatable = '<table class="datatable"  id="'+uid+'"><tr class="datatablehead">' + kwargs['tablehead'] + '</tr>'
            for col in columns:
                datatable = datatable.replace('_'+col+'_', model._meta.get_field_by_name(col)[0].verbose_name.title())
        else:
            datatable = '<table class="datatable"  id="'+uid+'"><tr class="datatablehead"><td></td>'
            for col in columns:
                datatable = datatable + '<td>'+model._meta.get_field_by_name(col)[0].verbose_name.title()+'</td>'
            datatable = datatable + '</tr>'
        strcounter = 0
    if len(dataset)>0:
        codemap = '<div id="'+uid+'_index" style="visibility: hidden; height:0px;">';
        for el in dataset:
            strcounter = strcounter + 1
            if hasattr(el, 'isfolder') and el.isfolder and 'parentcode' in kwargs and kwargs['parentcode'] == el.code:
                folderclass = 'class="folderTrue folderTrueopened"'
            elif hasattr(el, 'isfolder') and el.isfolder:
                folderclass = 'class="folderTrue folderTrueclosed"'
            else:
                folderclass = ''
            if 'tablehead' in kwargs:
                datatableblock = '<tr class="datatabledata" id="'+getattr(el, 'code')+'">'+kwargs['tablehead']+'</tr>'
                datatableblock = datatableblock.replace('_folderclass_', folderclass)
                codemap = codemap + getattr(el, 'code')+','
                for col in columns:
                    if bool(getattr(el, col)):
                        try:
                            value = str(getattr(el, col))
                        except:
                            value = getattr(el, col)
                    else:
                        value = ''
                    datatableblock = datatableblock.replace('_'+col+'_', value)
                datatable = datatable + datatableblock
            else:
                datatable = datatable+'<tr class="datatabledata" id="'+getattr(el, 'code')+'"><td width="10px" '+folderclass+'></td>'
                codemap = codemap + getattr(el, 'code')+','
                for col in columns:
                    if bool(getattr(el, col)):
                        try:
                            value = str(getattr(el, col))
                        except:
                            value = getattr(el, col)
                    else:
                        value = ''
                    datatable = datatable + '<td>'+value+'</td>'
                datatable = datatable+'</tr>'
        codemap = codemap[:len(codemap)-1] + '</div>'
    else:
        codemap = '<div id="'+uid+'_index" style="visibility: hidden; height:0px;"></div>'
    if len(columns)>0 or len(dataset)>0:
        datatable = datatable+'</table>'
#        script = "<script>$(document).ready(function () { Jdatatablerows['"+uid+"'] = "+codemap+";});</script>"
    else:
        datatable = ''
    if 'buttons' in kwargs:
        buts = '<div class="buttons '+uid+'" style="width:100%;">'
        for butt in kwargs['buttons']:
            buts = buts + '<img src="/static/img/buttons/'+butt+'.png" onclick="activeJdatatable = \''+uid+'\'; JdatatableAction(\''+butt+'\')">'
        buts = buts + '</div>'
        datatable = buts + datatable
    return codemap + datatable;
            
@login_required
def jdatatableaction(request):
    if request.method == 'POST':
        response = 'empty'
        if 'tableid' in request.POST and request.POST['tableid'] != '':
            tableid = request.POST['tableid']
            logger.debug(tableid)
            modelname = tableid[:tableid.find('_')]
            folderclass = request.POST.get('folderclass', None)
            model = jgetmodel(modelname)
            code = request.POST.get('code',None)
            logger.debug(code)
            if code:
                instance = model['model'].objects.filter(owner=request.user).filter(code=code)[0]
            else:   
                instance = model['model'](owner=request.user)
            operation = request.POST['operation']
            module = import_module(model['app']+'.views')
            logger.debug(module)
            if model and hasattr(module, operation):
                response = getattr(module, operation)(request, instance, folderclass)
        return HttpResponse(response)
        
def jgetmodel(modelname):
    for app in settings.INSTALLED_APPS:
        result = {'app':app, 'model':get_model(app, modelname)}
        if result['model']:
            return result
    return None

@login_required    
def jeditformprocessor(request):
    if request.method == 'POST':
        logger.debug(request.POST)
        if 'model' in request.POST: 
            model = jgetmodel(request.POST['model'])
            module = import_module(model['app'])
            logger.debug(str(module))
            if hasattr(module.views, 'editformprocessor'):
                response = getattr(module.views, 'editformprocessor')(request)
        return HttpResponse(response)
        
def entry(request, *args):
    return clients.views.entry(request, *args)