import os
import logging
import httplib2
from datetime import datetime, tzinfo
from pytz import timezone, utc

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
    csesoc_events = []

    # Filter by CSESOC_EVENTS_CREATOR
    events = filter(lambda a: a['creator']['email'] == settings.CSESOC_EVENTS_CREATOR, calendar['items'])

    # Filter by CSESoc in the title of the event
    events = filter(lambda a: 'csesoc' in a['summary'].lower() or 'cse soc' in a['summary'].lower(), events)

    # Filter by only upcoming events

    # Sort by date, soonest ones first

    # Limit to only 3 events
    events = events[0:3]

    # Format them according to our rules
    # FIXME: Make this prettier.
    for e in events:
        csesoc_e = {}
        try:
            csesoc_e['summary'] = e['summary']
        except:
            csesoc_e['summary'] = ''
        try:
            csesoc_e['description'] = e['description']
        except:
            csesoc_e['description'] = ''
        if e['start'].has_key('date'):
            start_day = datetime.strptime(e['start']['date'], "%Y-%m-%d")
            start_day = utc.localize(start_day).astimezone(timezone('Australia/Sydney'))
            start_day = start_day.strftime("%a %e %b")
            end_day = datetime.strptime(e['end']['date'], "%Y-%m-%d")
            end_day = utc.localize(end_day).astimezone(timezone('Australia/Sydney'))
            end_day = end_day.strftime("%a %e %b")
            time = '%s to %s'%(start_day, end_day)
        elif e['start'].has_key('dateTime'):
            start_day = datetime.strptime(e['start']['dateTime'], "%Y-%m-%dT%H:%M:%SZ")
            start_day = utc.localize(start_day).astimezone(timezone('Australia/Sydney'))
            start_day = start_day.strftime("%a %e %b from %l:%M%P")
            end_time = datetime.strptime(e['end']['dateTime'], "%Y-%m-%dT%H:%M:%SZ")
            end_time = utc.localize(end_time).astimezone(timezone('Australia/Sydney'))
            end_time = end_time.strftime("%l:%M%P")
            time = '%s to %s'%(start_day, end_time)
        else:
            continue
        csesoc_e['time'] = time
        csesoc_events.append(csesoc_e)

    return csesoc_events
