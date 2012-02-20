from Checkin.middleware import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import Member
import hs
import logging
from django.utils import simplejson
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def addEmails():
	noemails = Member.objects.filter(email='')
	for person in noemails:
		hsmatches = hs.search(person.firstname + ' ' + person.lastname)
		logger.info(len(hsmatches) + ' found for ' + person.firstname + ' ' + person.lastname)

def quiz_guess(request, pid):   
	message = {"mail": "", "givenName": ""}
	if request.is_ajax():
		results = hs.search(pid)
		person = results[0]
		logger.info(results)
		message['firstname'] = person.get('givenName')
		message['major'] = person.get('major')
		message['lastname'] = person.get('sn')
		message['email'] = person.get('mail')
		json = simplejson.dumps(message)
	return HttpResponse(json, mimetype='application/json')
	
#				matches = Member.objects.filter(firstname__iexact=form.cleaned_data['firstname'], lastname__iexact=form.cleaned_data['lastname'])
#		m = Member(idnum=request.POST['idnum'], pid=request.POST['pid'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], advertisingmethod=get_object_or_404(Advertisingmethod, name=request.POST['advertisingmethod']))
#		m.save()
