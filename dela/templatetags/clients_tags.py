from django import template
import datetime
import logging

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def cellheight(value):
    return (value.finish.hour*60+value.finish.minute-value.start.hour*60-value.start.minute)*38/120
    
@register.filter
def progress(incvalue):
    value = incvalue.progress
    return '#'+hex(255-int(255.0/100*value))[2:]+hex(int(255.0/100*value))[2:]+'00'
    

def stability(incvalue):
    now = datetime.datetime.utcnow()
    timeleft= (incvalue.finish.day-now.day)*60*24+(incvalue.finish.hour-now.hour)*60+(incvalue.finish.minute-now.minute)
    timeleft = timeleft+(incvalue.finish.month-now.month)*60*24*30+(incvalue.finish.year-now.year)*60*24*365
    timelength =  (incvalue.finish.day-incvalue.start.day)*60*24+(incvalue.finish.hour-incvalue.start.hour)*60+(incvalue.finish.minute-incvalue.start.minute)
    timelength = timelength+(incvalue.finish.month-incvalue.start.month)*60*24*30+(incvalue.finish.year-incvalue.start.year)*60*24*365
    logger.debug('timelength: '+str(timelength))
    logger.debug('timeleft: '+str(timeleft))
    if timelength<=timeleft:
        return 100
    if timeleft<=0:
        if incvalue.progress == 100:
            return 100
        else:
            return 0
    speed = float(incvalue.progress)/(timelength-timeleft)
    speedneed = float(100-incvalue.progress)/timeleft
    stability = speed/speedneed
    logger.debug('speed: '+str(speed))
    logger.debug('speedneed: '+str(speedneed))
    logger.debug('stability: '+str(stability))
    if stability>1:
        return 100
    else:
        return stability*100
    
@register.filter   
def stabilitycolor(incvalue):
    value = stability(incvalue)
    return 'rgb('+str(255-int(round(255.0/100*value)))+', '+str(int(round(255.0/100*value)))+',0)'
    
@register.filter   
def stabilityvalue(incvalue):
    value = stability(incvalue)
    return int(value)