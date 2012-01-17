from django.conf import settings

def sponsors_list(request):
  from csesoc.sponsors.models import Sponsor
  sponsors = Sponsor.objects.order_by('-amount_paid', 'name')
  return { 'sponsors' : sponsors }

def csesoc_events(request):
    from csesoc.gcal.views import get_csesoc_events
    return {'csesoc_events' : get_csesoc_events()}
