from django.db import models

class Event(models.Model):
	date = models.DateField()	

	def __unicode__(self):
		return self.date.__str__()

class Advertisingmethod(models.Model):
	name = models.CharField(max_length = 30)	
	def __unicode__(self):
		return self.name


class Member(models.Model):
	idnum = models.IntegerField()
	pid = models.CharField(max_length = 20)
	firstname = models.CharField(max_length = 20)
	lastname = models.CharField(max_length = 20)
	advertisingmethod = models.ForeignKey(Advertisingmethod)
	def __unicode__(self):
		return self.pid


class Record(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	def __unicode__(self):
		return self.member.pid + " " + self.event.date.__str__()
