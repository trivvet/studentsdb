# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Exam(models.Model):
	class Meta(object):
		verbose_name = u"Екзамен"
		verbose_name_plural = u"Екзамени"
		
	matter = models.CharField(
		verbose_name = u"Предмет",
		max_length = 256,
		blank = False,
		null = False)
		
	time = models.DateTimeField(
		verbose_name = u"Час проведення",
		blank = False,
		null = False)
		
	teacher = models.CharField(
		verbose_name = u"Викладач",
		max_length = 256,
		blank = False,
		null = False)
		
	group_exam = models.ForeignKey('Group',
		verbose_name = u"Група",
		blank = False,
		null = False)
		
	def __unicode__(self):
		return u"%s (%s)" % (self.matter, self.group_exam.title)
