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
	advertisingmethod = models.CharField(max_length = 20,required=False)#models.ForeignKey(Advertisingmethod)
	referername = models.CharField(max_length = 20,required=False)
	paymentinfo = models.CharField(max_length = 20,required=False)
	event1_22_11 = models.CharField(max_length = 20,required=False)
	event9_8_11 = models.CharField(max_length = 20,required=False)
	event9_10_11 = models.CharField(max_length = 20,required=False)
	event9_15_11 = models.CharField(max_length = 20,required=False)
	event9_29_11 = models.CharField(max_length = 20,required=False)
	event10_6_11 = models.CharField(max_length = 20,required=False)
	event10_13_11 = models.CharField(max_length = 20,required=False)
	eventsocial10_15= models.CharField(max_length = 20,required=False)
	event10_20_11 = models.CharField(max_length = 20,required=False)
	event10_27_11 = models.CharField(max_length = 20,required=False)
	event11_3_11 = models.CharField(max_length = 20,required=False)
	event11_10_11 = models.CharField(max_length = 20,required=False)
	event12_1_11 = models.CharField(max_length = 20,required=False)
	event1_19_2012 = models.CharField(max_length = 20,required=False)
	event1_26_2012 = models.CharField(max_length = 20,required=False)
	event2_2_2012 = models.CharField(max_length = 20,required=False)
	eventSocial2_4_2012 = models.CharField(max_length = 20,required=False)
	event2_9_2012 = models.CharField(max_length = 20,required=False)
	def __unicode__(self):
		return self.pid
	def statsID(self):
		return self.firstname + " " + self.lastname


class Record(models.Model):
	member = models.ForeignKey(Member)
	event = models.ForeignKey(Event)
	def __unicode__(self):
		return self.member.firstname + " " + self.member.lastname + " " + self.event.date.__str__()
