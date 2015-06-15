from django import forms
from projects.models import Project, Task
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.forms.widgets import *
from django.utils import timezone
from django.contrib.auth.models import User

class Html5DateTimeInput(forms.DateInput):
    
    input_type = 'datetime-local'

class ProjectEditForm (ModelForm):
    class Meta:
        model = Project
        fields = ['code', 'topic', 'start', 'finish', 'content', 'admins', 'members']
        widgets = {
            'code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'topic': forms.TextInput(attrs={'maxlength': '100'}),
            'start': Html5DateTimeInput(),
            'finish': Html5DateTimeInput()
        }
        
class TaskEditForm (ModelForm):
    projectid    = forms.CharField(max_length=9, required=False, initial='', widget=forms.HiddenInput())

    class Meta:
        model = Task
        fields = ['code', 'project', 'parent', 'liable', 'topic', 'start', 'finish',
                  'content', 'finished', 'result',
                  'checklist', 'attaches',
                  'progress', 'status', 'statushist', 'admins', 'liables', 'observers', 'projectid']
        widgets = {
            'code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'topic': forms.TextInput(attrs={'maxlength': '100'}),
            'start': Html5DateTimeInput(),
            'finish': Html5DateTimeInput(),
            'finished': Html5DateTimeInput(),
            'checklist': forms.TextInput(attrs={'readonly': 'readonly'}),
            'attaches': forms.TextInput(attrs={'readonly': 'readonly'}),
            'statushist': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
