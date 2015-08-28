# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from ..models.journal import Student_visiting
from ..models.monthjournal import MonthJournal
from ..models.students import Student
from ..models.groups import Group
from django.views.generic.base import TemplateView
from datetime import datetime, date

class JournalView(TemplateView):
	template_name = 'students/journal.html'
	
	def get_context_data(self, **kwargs):
		context = super(JournalView, self).get_context_data(**kwargs)
		today = datetime.today()
		month = date(today.year, today.month, 1)
		
		context['prev_month'] = '2015-07-01'
		context['next_month'] = '2015-09-01'
		context['year'] = 2015
		context['cur_month'] = '2015-08-01'
		context['month_verbose'] = u'Липень'
		
		context['month_header'] = [
			{'day': 1, 'verbose': 'Пн'},
			{'day': 2, 'verbose': 'Вт'},
			{'day': 3, 'verbose': 'Ср'},
			{'day': 4, 'verbose': 'Чт'},
			{'day': 5, 'verbose': 'Пт'}]
			
		queryset = Student.objects.order_by('first_name')
		
		update_url = reverse('journal') 
		
		students = []
		
		for student in queryset:
			days = []
			for day in range(1,6):
				days.append({
					'day': day,
					'present': True,
					'date': date(2015, 8, day).strftime('%Y-%m-%d'),
					})
			students.append({
				'full_name': u'%s %s' % (student.first_name, student.last_name),
				'days': days,
				'id': student.id,
				'updade_url': update_url,
				})
		
		pages = []
		k = 0
		if len(students) % 10 == 0:
			k = len(students) / 10
		else:
			k = len(students) / 10 + 1
		for page in range(k):
			pages.append(str(page+1))
		context['pages'] = pages
			
		page = int(self.request.GET.get('page', '1'))
		context['page'] = (page - 1) * 10
		if len(pages) <= 1:
			context['students'] = students
		else:
			context['students'] = students[(page - 1)*10:page*10]
		
		return context

def journal_list(request):
	students = Student_visiting.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'student_name__first_name'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
		students = students.order_by('id')
		
	pages = []
	k = 0
	if not students.count() % 3 == 0:
		k = 1
	for i in range(students.count() / 5 + k):
		pages.append(str(i+1))
		
	number_page = int(request.GET.get('page', '1'))
	if number_page > len(pages):
		number_page = len(pages) - 3
		number_page = len(pages)
	students = students[number_page * 3 - 3: number_page * 3]
		
	days = '111111111111111111111111111111'	
	
	groups = Group.objects.all()
	return render(request, 'students/journal_list.html', {'students': students, 'groups': groups, 'pages': pages, 'days': days})
