# -*- coding: utf-8 -*-

from django.db import models

class Group(models.Model):
	"""Group Model"""
	
	class Meta(object):
		verbose_name = u"Група"
		verbose_name_plural = u"Групи"
	
	title = models.CharField(
		max_length=250,
		blank=False,
		unique=True,
		error_messages={'unique': 'Група з такою назвою вже існує'},
		verbose_name=u"Назва")
	
	leader = models.OneToOneField('Student',
		verbose_name=u"Староста",
		blank=True,
		null=True,
		error_messages={'unique': 'Група з таким старостою вже існує'},
		on_delete=models.SET_NULL)
		
	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки")
	
	def __unicode__(self):
		if self.leader:
			return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
		else:
			return u"%s" % (self.title,)
			
