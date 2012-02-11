from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from django.shortcuts import get_object_or_404
from datetime import date
from Checkin.middleware import *
import logging

logger = logging.getLogger(__name__) 

class SigninForm(forms.Form):
	idnum = forms.CharField();
	def is_valid(self):
		return True;

class SigninForm2(forms.Form):
	vtpid = forms.CharField()
	firstname = forms.CharField()
	lastname = forms.CharField()
	advertisingmethod = forms.ModelChoiceField(queryset=Advertisingmethod.objects.all())

class AddAdvertisingmethodForm(forms.Form):
	name = forms.CharField()

def index(request):
	return render_to_response('signin.html', {'': ''}, context_instance=RequestContext(request))

def getToday():
	return Event.objects.get(date=date.today())

def checkinMember(member):
	try:
		res = Record.objects.get_or_create(member=member, event=getToday())
		return res[1]
	except Record.DoesNotExist:
		raise Http403
	except Event.DoesNotExist:
		raise Http403

def addAdvertisingmethod(request, trimmed_idnum):
	return render_to_response('new_advertisingmethod.html', {'idnum': trimmed_idnum}, context_instance=RequestContext(request))

def createNewAdvertisingmethod(request):
	name = request.POST['name']
	trimmed_idnum = request.POST['idnum']
	if len(Advertisingmethod.objects.filter(name=name)) == 0:
		o = Advertisingmethod(name=name)
		o.save()
	return render_to_response('newrecord.html', {'idnum': trimmed_idnum, 'choices': Advertisingmethod.objects.all()}, context_instance=RequestContext(request))

def signin(request):
	trimmed_idnum = int(request.POST['idnum'][0:10])
	matchCount = len(Member.objects.filter(idnum=trimmed_idnum))
	logger.info('signin request for ' + str(trimmed_idnum) + ' matched ' + str(matchCount) + ' members in database')
	if matchCount == 1:
		# Member already exists, add attendance record
		if checkinMember(Member.objects.filter(idnum=trimmed_idnum)[0]):
			return render_to_response('signin_success.html', {'': ''}, context_instance=RequestContext(request))
		else:
			return render_to_response('signin_duplicate.html', {'': ''}, context_instance=RequestContext(request))
	else:
		return render_to_response('newrecord.html', {'idnum': trimmed_idnum, 'choices': Advertisingmethod.objects.all()}, context_instance=RequestContext(request))

def createNewRecord(request):
	# Create a new record, add attendance record
	try:
		m = Member(idnum=request.POST['idnum'], pid=request.POST['pid'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], advertisingmethod=get_object_or_404(Advertisingmethod, name=request.POST['advertisingmethod']))
		m.save()
		checkinMember(m)
	except Event.DoesNotExist:
		raise BadUserCreation
	return render_to_response('signin_success.html', {'': ''}, context_instance=RequestContext(request))