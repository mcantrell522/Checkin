from django.shortcuts import render_to_response
from django.template import RequestContext
from sec.signin.models import *

def index(request):
	records = Record.objects.all().values('date')
	
	attend_member = {}
	attend_society = {}
	
	for member in Member.objects.all():
		attend_member[member.pid] = []
		attend_member[member.pid].append(member.firstname + " " + member.lastname)
		attend_member[member.pid].append(member.society.name)
		
	for society in Society.objects.all():
		attend_society[society.name] = []
		attend_society[society.name].append(society.name)
	
	dates = [];
	for r in records:
		if r['date'] not in dates:
			dates.append(r['date'])
			
	dates.sort()
	
	for date in dates:
		societies_today = []
		for member in attend_member:
			attend = len(Record.objects.filter(member=Member.objects.get(pid=member), date=date))
			attend_member[member].append(attend)
#			if attend == 1:
#				societies_today.append(Record.objects.get(member=Member.objects.get(pid=member), date=date).society.name)
#		for society in attend_society:
#			if society.name in societies_today:
#				attend_society[society].append("1")
#			else:
#				attend_society[society].append("0")
	
#	print attend_member
#	for value in attend_member.items():
#		print value
#		for v in value:
#			print v
	
	return render_to_response('stats.html', {'members': Member.objects.all(), context_instance=RequestContext(request))
