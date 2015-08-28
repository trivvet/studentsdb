# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from models.students import Student
from models.groups import Group
from models.monthjournal import MonthJournal
from models.journal import Student_visiting
from models.exams import Exam

def make_copy(modeladmin, request, queryset):
	pass
make_copy.short_description = u"Копіювати обраних Студентів" 

class StudentFormAdmin(ModelForm):
	
	def clean_student_group(self):
		"""Check if student is leader in any group
		
		If yes, then ensure it's the same as selected. """
		# get group where current student is a leader
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи.',
				code='invalid')
				
		return self.cleaned_data['student_group']
		
class GroupFormAdmin(ModelForm):
	
	def clean_leader(self):
		"""Check if student is leader in any group
		
		If yes, then ensure it's the same as selected. """
		# get group where current student is a leader
		student = Student.objects.get(pk=self.cleaned_data['leader'].id)
		if self.instance.id != student.student_group.id:
			raise ValidationError(u'Вибраний староста навчається в іншій групі',
				code='invalid')
				
		return self.cleaned_data['leader']

class StudentAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['first_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['first_name', 'last_name', 'middle_name', 'ticket',
		'notes']
	actions = [make_copy]
	form = StudentFormAdmin
		
	def view_on_site(self, obj):
		return reverse('students_edit', kwargs = {'pk': obj.id})
		
class GroupAdmin(admin.ModelAdmin):
	list_display = ['title', 'leader']
	list_display_links = ['title']
	list_editable = ['leader']
	ordering = ['title']
	list_filter = ['leader']
	list_per_page = 3
	search_fields = ['title']
	form = GroupFormAdmin
		
	def view_on_site(self, obj):
		return reverse('groups_edit', kwargs = {'pk': obj.id})

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)
admin.site.register(Student_visiting)
admin.site.register(Exam)
