from django import forms
from clients.models import Client
from contacts.models import Contact
from django.utils.translation import ugettext as _
from django.forms import ModelForm
        
class ContactEditForm (ModelForm):
    owner 		= forms.ModelChoiceField(queryset=Client.objects.filter(isfolder=False), required=False)
    fio 		= forms.CharField(max_length=255, required=True, label=_('FIO'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    email 		= forms.EmailField(required=False, label=_('Email'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    birthday	= forms.DateField(required=False, label=_('Birthday'))
    position	= forms.CharField(max_length=100, required=False, label=_('Position'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    phone		= forms.CharField(max_length=100, required=False, label=_('Phone'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    
    class Meta:
        model = Client
        fields = ['fio','email', 'birthday','position', 'phone']
        

class ClientEditForm (ModelForm):
#	isfolder 	= forms.BooleanField()
#   code 		= forms.CharField(max_length=9, required=True, label='Code', widget=forms.TextInput(attrs={'placeholder': 'code', 'readonly': 'readonly'}))
    parent      = forms.ModelChoiceField(queryset=Client.objects.filter(isfolder=True), required=False, label=_('Parent'))
    code 		= forms.CharField(max_length=9, required=False, label=_('Code'), widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name 		= forms.CharField(max_length=255, required=False, label=_('Name'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    iscompany 	= forms.BooleanField(label=_('Is company'), required=False)
    INN 		= forms.CharField(max_length=12, required=False, label=_('INN'))
    KPP 		= forms.CharField(max_length=9, required=False, label=_('KPP'))
    email 		= forms.EmailField(required=False, label=_('Email'))
    uradress	= forms.CharField(max_length=150, required=False, label=_('Company Address'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    factadress	= forms.CharField(max_length=150, required=False, label=_('Post address'))
    phone		= forms.CharField(max_length=30, required=False, label=_('Phone'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    fax			= forms.CharField(max_length=30, required=False, label=_('Fax'))
    site		= forms.CharField(max_length=50, required=False, label=_('Site'))
    isfolder 	= forms.BooleanField(required=False, initial='', widget=forms.HiddenInput())
            
    class Meta:
        model = Client
        fields = ['parent','code', 'name', 'iscompany', 'INN', 'KPP', 'email', 'uradress', 'factadress', 'phone', 'fax', 'site']
        
class ClientFolderEditForm (ModelForm):
    parent      = forms.ModelChoiceField(queryset=Client.objects.filter(isfolder=True), required=False)
    code 		= forms.CharField(max_length=9, required=False, label=_('Code'), widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name 		= forms.CharField(max_length=255, required=False, label=_('Name'), widget=forms.TextInput(attrs={'maxlength': '100'}))
    isfolder 	= forms.BooleanField(required=False, initial='true', widget=forms.HiddenInput())
    
    class Meta:
        model = Client
        fields = ['parent','code', 'name']