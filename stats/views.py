from django.shortcuts import render_to_response
from django.template import RequestContext
from sec.signin.models import *

def index(request):
	records = Record.objects.all()
	
	attend_member = {}
	attend_society = {}
	
	for member in Member.objects.all():
		attend_member[member.pid] = []
		attend_member[member.pid].append(member.firstname + " " + member.lastname)
		attend_member[member.pid].append(member.society.name)
		attend_member[member.pid].append([])
		for g in GAM.objects.all():
			try:
				record = Record.objects.get(member=member, gam=g)
				attend_member[member.pid][2].append(1)
			except:		
				attend_member[member.pid][2].append(0)
		attend_member[member.pid].append(100 * sum(attend_member[member.pid][2])/len(attend_member[member.pid][2]))

	for s in Society.objects.all():
		if s.name == 'Individual':
			continue;
		attend_society[s.name] = []
		attend_society[s.name].append(s.name)
		attend_society[s.name].append([])
		for g in GAM.objects.all():
			ok = 0
			for member in Member.objects.all():
				try:
					record = Record.objects.get(member=member, gam=g)
					if record.member.society == s:
						ok = 1
				except:
					ok = ok
			attend_society[s.name][1].append(ok)

		attend_society[s.name].append(100 * sum(attend_society[s.name][1])/len(attend_society[s.name][1]))
	
	return render_to_response('stats.html', {'gam': GAM.objects.all(), 'attend': attend_member, 'attend2': attend_society}, context_instance=RequestContext(request))
