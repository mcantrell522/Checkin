from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from sec.signin.models import *
from django.shortcuts import get_object_or_404
from datetime import date

class SigninForm(forms.Form):
	idnum = forms.CharField();
	def is_valid(self):
		return True;

class SigninForm2(forms.Form):
	vtpid = forms.CharField()
	firstname = forms.CharField()
	lastname = forms.CharField()
	society = forms.ModelChoiceField(queryset=Society.objects.all())

class AddOrgForm(forms.Form):
	name = forms.CharField()

def index(request):
	return render_to_response('signin.html', {'': ''}, context_instance=RequestContext(request))

def getToday():
	return GAM.objects.get(date=date.today())

def checkinMember(member):
	res = Record.objects.get_or_create(member=member, gam=getToday())
	return res[1]



def addOrganization(request, trimmed_idnum):
	return render_to_response('new_organization.html', {'idnum': trimmed_idnum}, context_instance=RequestContext(request))

def createNewOrganization(request):
	name = request.POST['name']
	trimmed_idnum = request.POST['idnum']
	if len(Society.objects.filter(name=name)) == 0:
		o = Society(name=name)
		o.save()
	return render_to_response('newrecord.html', {'idnum': trimmed_idnum, 'choices': Society.objects.all()}, context_instance=RequestContext(request))

def signin(request):
	trimmed_idnum = int(request.POST['idnum'][1:10])
	if len(Member.objects.filter(idnum=trimmed_idnum)) == 1:
		# Member already exists, add attendance record
		if checkinMember(Member.objects.filter(idnum=trimmed_idnum)[0]):
			return render_to_response('signin_success.html', {'': ''}, context_instance=RequestContext(request))
		else:
			return render_to_response('signin_duplicate.html', {'': ''}, context_instance=RequestContext(request))
	else:
		return render_to_response('newrecord.html', {'idnum': trimmed_idnum, 'choices': Society.objects.all()}, context_instance=RequestContext(request))

def createNewRecord(request):
	# Create a new record, add attendance record
	m = Member(idnum=request.POST['idnum'], pid=request.POST['pid'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], society=get_object_or_404(Society, name=request.POST['society']))
	m.save()
	checkinMember(m)
	return render_to_response('signin_success.html', {'': ''}, context_instance=RequestContext(request))

