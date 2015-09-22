# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam

@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	
	student = kwargs['instance']
	if kwargs['created']:
		logger.info('Student added: %s %s (ID: %d)', student.first_name,
			student.last_name, student.id)
			
	else:
		logger.info('Student updated: %s %s (ID: %d)', student.first_name,
			student.last_name, student.id)
			
@receiver(post_delete, sender=Student)
def log_student_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	
	student = kwargs['instance']
	logger.info('Student_deleted: %s %s (ID: %d)', student.first_name, 
		student.last_name, student.id)
		
@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	
	group = kwargs['instance']
	if kwargs['created']:
		logger.info('Group added: %s (ID: %d)', group.title, group.id)
			
	else:
		logger.info('Group updated: %s (ID: %d)', group.title, group.id)
			
@receiver(post_delete, sender=Group)
def log_group_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	
	group = kwargs['instance']
	logger.info('Group deleted: %s (ID: %d)', group.title, group.id)
	
@receiver(post_save, sender=Exam)
def log_exam_updated_added_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	
	exam = kwargs['instance']
	if kwargs['created']:
		logger.info('Exam added: %s %s', exam.matter, exam.group_exam)		
	else:
		logger.info('Exam updated: %s %s', exam.matter, exam.group_exam)
			
@receiver(post_delete, sender=Exam)
def log_exam_delete_event(sender, **kwargs):
	logger = logging.getLogger(__name__)
	
	exam = kwargs['instance']
	logger.info('Exam deleted: %s %s', exam.matter, exam.group_exam)
