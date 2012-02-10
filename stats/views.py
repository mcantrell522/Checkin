from Checkin.signin.models import Record, Member, Event, Advertisingmethod
from django.shortcuts import render_to_response
from django.template import RequestContext
from signin.models import *

def index(request):
	records = Record.objects.all()
	
	attend_member = {}
	attend_advertisingmethod = {}
	
	for member in Member.objects.all():
		attend_member[member.pid] = []
		attend_member[member.pid].append(member.firstname + " " + member.lastname)
		try:
			attend_member[member.pid].append(member.advertisingmethod.name)
		except:
			attend_member[member.pid].append(member.advertisingmethod)
		attend_member[member.pid].append([])
		for g in Event.objects.all():
			try:
				record = Record.objects.get(member=member, event=g)
				attend_member[member.pid][2].append(1)
			except:		
				attend_member[member.pid][2].append(0)
		attend_member[member.pid].append(100 * sum(attend_member[member.pid][2])/len(attend_member[member.pid][2]))

	for s in Advertisingmethod.objects.all():
		if s.name == 'Individual':
			continue;
		attend_advertisingmethod[s.name] = []
		attend_advertisingmethod[s.name].append(s.name)
		attend_advertisingmethod[s.name].append([])
		for g in Event.objects.all():
			ok = 0
			for member in Member.objects.all():
				try:
					record = Record.objects.get(member=member, event=g)
					if record.member.advertisingmethod == s:
						ok = 1
				except:
					ok = ok
			attend_advertisingmethod[s.name][1].append(ok)

		attend_advertisingmethod[s.name].append(100 * sum(attend_advertisingmethod[s.name][1])/len(attend_advertisingmethod[s.name][1]))
	
	return render_to_response('stats.html', {'event': Event.objects.all(), 'attend': attend_member, 'attend2': attend_advertisingmethod}, context_instance=RequestContext(request))
