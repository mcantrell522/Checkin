from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from django.shortcuts import get_object_or_404
from datetime import date
from Checkin.middleware import *
import logging

logger = logging.getLogger(__name__)

def header_search():
	cat_values = []
	cats_list = Member.objects.all()
	for cat in cats_list:
		cat_values.append((cat.statsID))
	return cat_values
	
class SigninForm(forms.Form):
	idnum = forms.CharField(required=True);
	firstname = forms.CharField(required=False)
	lastname = forms.CharField(required=False)
	choices = forms.ChoiceField(widget=forms.Select, choices=header_search(),required=False)
	associate = forms.BooleanField(required=False)
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
	return render_to_response('signin.html', {'choices': Member.objects.all()}, context_instance=RequestContext(request))

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
	if request.method == 'POST': # If the form has been submitted...
		form = SigninForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			logger.info('form valid')
			idnum = form.cleaned_data['idnum']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			needToAssociate = form.cleaned_data['associate']
			if needToAssociate:
				logger.info('Need to associate ID with existing member')
				matches = Member.objects.filter(firstname__iexact=form.cleaned_data['firstname'], lastname__iexact=form.cleaned_data['lastname'])
				logger.info('Finding matches for member ' + form.cleaned_data['firstname'] + ' ' + form.cleaned_data['lastname'])
				if len(matches) == 1: #all is well, make the id association
					logger.info('Found 1 match, storing ID')
					matches[0].idnum = idnum
					matches[0].save()
				elif len(matches) > 1:
					logger.info('Found too many (' + len(matches) + ') matches, need to fix')
					return render_to_response('newrecord.html', {'idnum': idnum, 'choices': Advertisingmethod.objects.all()}, context_instance=RequestContext(request))
				else:
					logger.info('Found no matches, need to make new member.')
					return render_to_response('newrecord.html', {'idnum': idnum, 'choices': Advertisingmethod.objects.all()}, context_instance=RequestContext(request))
			else:
				logger.info('Looking up existing member for ID')
				matches = Member.objects.filter(idnum=idnum)
				logger.info('signin request for ' + str(idnum) + ' matched ' + str(len(matches)) + ' members in database')
			if len(matches) == 1:
					# Member already exists, add attendance record
					if checkinMember(matches[0]):
						return render_to_response('signin_success.html', {'': ''}, context_instance=RequestContext(request))
					else:
						return render_to_response('signin_duplicate.html', {'': ''}, context_instance=RequestContext(request))
		else:
					return render_to_response('newrecord.html', {'idnum': idnum, 'choices': Advertisingmethod.objects.all()}, context_instance=RequestContext(request))
			#return HttpResponseRedirect('/thanks/') # Redirect after POST
	else:
			form = SigninForm() # An unbound form

			return render_to_response('signin.html', {'form': form, 'choices' : Advertisingmethod.objects.all() })


def createNewRecord(request):
	# Create a new record, add attendance record
	try:
		m = Member(idnum=request.POST['idnum'], pid=request.POST['pid'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], advertisingmethod=get_object_or_404(Advertisingmethod, name=request.POST['advertisingmethod']))
		m.save()
		checkinMember(m)
	except Event.DoesNotExist:
		raise BadUserCreation
	return render_to_response('signin_success.html', {'': ''}, context_instance=RequestContext(request))
