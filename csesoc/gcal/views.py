import os
import logging
import httplib2

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from apiclient.discovery import build

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

http = httplib2.Http()
service = build(
        serviceName="calendar", 
        version="v3", 
        http=http, 
        developerKey=settings.GCAPI_KEY)
calendar = service.events().list(calendarId=settings.CSE_STUDENT_CALENDAR_ID).execute()

def gcal_index(request):
    csesoc_events = get_csesoc_events()

    return render_to_response('gcal.html', {
                'calendar' : calendar,
                'calendar_name': calendar['summary'],
                'calendar_desc': calendar['description'],
                'csesoc_events': csesoc_events,
                }, context_instance=RequestContext(request))

def get_csesoc_events():
    return filter(lambda a: a['creator']['email'] == settings.CSESOC_EVENTS_CREATOR, calendar['items'])
