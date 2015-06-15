from django import forms
from dela.models import Dela
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.forms.widgets import *
from django.utils import timezone

class Html5DateTimeInput(forms.DateInput):
    
    input_type = 'datetime-local'

class DelaEditForm(ModelForm):
    code        = forms.CharField(max_length=9, label=_('Code'), required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    topic         = forms.CharField(max_length=255, required=False, label=_('Topic'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    start    = forms.DateTimeField(label=_("Start"), required=False, widget=Html5DateTimeInput())
    sendstartsms = forms.BooleanField(required=False, label=_('Sendstartsms'))
    sendstartmail = forms.BooleanField(required=False, label=_('Sendstartmail'))
    finish    = forms.DateTimeField(label=_("Finish"), required=False, widget=Html5DateTimeInput())
    sendfinishsms = forms.BooleanField(required=False, label=_('Sendfinishsms') )
    sendfinishmail = forms.BooleanField(required=False, label=_('Sendfinishmail'))
    content    = forms.CharField(widget = forms.Textarea, required=False, label=_('Content'))
    result       = forms.CharField(widget = forms.Textarea, required=False, label=_('Result'))
    finished    = forms.DateTimeField(label=_("Finished"), required=False, widget=Html5DateTimeInput())
    attache     = forms.FileField(label=_("Attache"), required=False)
    deladate    = forms.CharField(max_length=15, required=False, initial='', widget=forms.HiddenInput())
       
    class Meta:
        model = Dela
        fields = ['code', 'topic', 'start', 'sendstartsms', 'sendstartmail', 'finish', 'sendfinishsms', 'sendfinishmail', 'content', 'result', 'finished', 'attache']
        
