# -*- coding: utf-8 -*-

import datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from clients.views import entry
from dela.models import Dela, Message
from django.core.management.base import NoArgsCommand
import smtplib
from email.mime.text import MIMEText
import sys
from multiuser.models import UserInfo
import logging

logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        sendmail('s')
     
def sendmail(request):
    delas = Message.objects.filter(sendsms=True).filter(sendtime__lte=datetime.datetime.now())
    for delo in delas:
        sendemail2(delo, 'sms')
        delo.delete()
        
    delas = Message.objects.filter(sendmail=True).filter(sendtime__lte=datetime.datetime.now())
    for delo in delas:
        sendemail2(delo, 'mail')
        delo.delete()


#    send_mail('Subject here', 'Here is the message.', 'joerespublic@yandex.ru', ['ggbystrov@yandex.ru'], fail_silently=False)

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.yandex.ru:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    
def sendemail2(delo, way):
    usert = UserInfo.objects.filter(owner=delo.owner)
    if usert.count()==1:
        delta = datetime.timedelta(0,60*60*usert[0].timezone)
    else:
        delta = datetime.timedelta(0,0)
    sender = 'www.JoomboCRM.tk <joerespublic@yandex.ru>'
    #Адрес получателя:
    if way == 'mail':
        recipient = delo.owner.email
    elif way == 'sms' and usert.count()==1:
        recipient = usert[0].phone+'@er34.send.smsc.ru'
    else:
        return -1;
    #79219785896@er34.send.smsc.ru
    #Тема письма:
    subj = delo.topic+' '+str(delo.sendtime+delta)
    #Текст сообщения:
    message = delo.content
        #Создаем письмо (заголовки + текст):
    msg = MIMEText(message, "", "utf-8")
    msg['Subject'] = subj
    msg['From'] = sender
    msg['To'] = recipient
 
    #Параметры авторизации
    #Логин:
    username = 'joerespublic@yandex.ru'
    #Пароль:
    password = 'By,fhvfktywbz'
         
    #Инициализвция соединения с сервером Gmail по smtp
    server = smtplib.SMTP('smtp.yandex.ru:587')
    #Выводим лог работы с сервером (для отладки)
    server.set_debuglevel(1);
    #Переходим в защищенное режим (TLS)
    server.starttls()
    #Авторизация
    server.login(username, password)
    #Отправляем письмо
    server.sendmail(sender, recipient, msg.as_string())
    
#    recipient = '@er34.send.smsc.ru'
#    logger.debug(recipient)
#    msg['To'] = recipient
    
#    server.sendmail(sender, recipient, msg.as_string())
    #Закрываем соединение с сервером
    server.quit()