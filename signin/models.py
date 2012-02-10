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
	idnum = models.CharField(max_length = 20)
	pid = models.CharField(max_length = 20)
	firstname = models.CharField(max_length = 20)
	lastname = models.CharField(max_length = 20)
	email = models.CharField(max_length = 20)
	studenttype = models.CharField(max_length = 20)
	membershipexpiration = models.CharField(max_length = 20) 
	advertisingmethod = models.CharField(max_length = 20)#models.ForeignKey(Advertisingmethod)
	referername = models.CharField(max_length = 20)
	paymentinfo = models.CharField(max_length = 20)
	event1_22_11 = models.CharField(max_length = 20)
	event9_8_11 = models.CharField(max_length = 20)
	event9_10_11 = models.CharField(max_length = 20)
	event9_15_11 = models.CharField(max_length = 20)
	event9_29_11 = models.CharField(max_length = 20)
	event10_6_11 = models.CharField(max_length = 20)
	event10_13_11 = models.CharField(max_length = 20)
	eventsocial10_15= models.CharField(max_length = 20)
	event10_20_11 = models.CharField(max_length = 20)
	event10_27_11 = models.CharField(max_length = 20)
	event11_3_11 = models.CharField(max_length = 20)
	event11_10_11 = models.CharField(max_length = 20)
	event12_1_11 = models.CharField(max_length = 20)
	event1_19_2012 = models.CharField(max_length = 20)
	event1_26_2012 = models.CharField(max_length = 20)
	event2_2_2012 = models.CharField(max_length = 20)
	eventSocial2_4_2012 = models.CharField(max_length = 20)
	event2_9_2012 = models.CharField(max_length = 20)
	def __unicode__(self):
		return self.pid


class Record(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	def __unicode__(self):
		return self.member.pid + " " + self.event.date.__str__()
