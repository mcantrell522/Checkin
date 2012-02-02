from django.db import models

class GAM(models.Model):
	date = models.DateField()	

	def __unicode__(self):
		return self.date.__str__()

class Society(models.Model):
	name = models.CharField(max_length = 30)	
	def __unicode__(self):
		return self.name


class Member(models.Model):
	idnum = models.IntegerField()
	pid = models.CharField(max_length = 20)
	firstname = models.CharField(max_length = 20)
	lastname = models.CharField(max_length = 20)
	society = models.ForeignKey(Society)
	def __unicode__(self):
		return self.pid


class Record(models.Model):
	member = models.ForeignKey(Member)
	gam = models.ForeignKey(GAM)
	def __unicode__(self):
		return self.member.pid + " " + self.gam.date.__str__()
