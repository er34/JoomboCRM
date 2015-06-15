from django import forms
from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.forms.widgets import *
from django.utils import timezone
import html5.forms.widgets as widgets

class Html5DateInput(forms.DateInput):
    
    input_type = 'date'

class ContactEditForm (ModelForm):
#   isfolder   = forms.BooleanField()
#   code        = forms.CharField(max_length=9, required=True, label='Code', widget=forms.TextInput(attrs={'placeholder': 'code', 'readonly': 'readonly'}))
    code        = forms.CharField(max_length=9, label=_('Code'), required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fio         = forms.CharField(max_length=255, required=False, label=_('FIO'), widget=forms.TextInput(attrs={'maxlength': '255'}))
    email       = forms.EmailField(required=False, label=_('Email'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    birthday    = forms.DateField(label=_("Birthday"), required=False, widget=Html5DateInput())
    position    = forms.CharField(max_length=150, required=False, label=_('Job position'), widget=forms.TextInput(attrs={'maxlength': '150'}))
    phone       = forms.CharField(max_length=30, required=False, label=_('Phone'), widget=forms.TextInput(attrs={'maxlength': '30'}))
    clientid    = forms.CharField(max_length=9, required=False, initial='', widget=forms.HiddenInput())
       
    class Meta:
        model = Contact
        fields = ['code', 'fio', 'email', 'birthday', 'position', 'phone']