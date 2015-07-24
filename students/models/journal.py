# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Student_visiting(models.Model):
	
	class Meta(object):
		verbose_name = u"Відвідування"
		verbose_name_plural = u"Відвідування"
		
	student_name = models.OneToOneField('Student',
		verbose_name = u"Студент",
		blank = False,
		null = True)
		
	visiting = models.IntegerField(
		max_length = 5,
		blank = True,
		null = True)

	def __unicode__(self):
		return "%s %s" % (self.student_name.first_name, self.student_name.last_name)
		
