# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from ..models.journal import Student_visiting
from ..models.monthjournal import MonthJournal
from ..models.students import Student
from ..models.groups import Group
from django.views.generic.base import TemplateView
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from ..views.paginator import page_scroll
import pdb
from ..util import get_current_group

class JournalView(TemplateView):
	template_name = 'students/journal.html'
	
	def get_context_data(self, **kwargs):
		context = super(JournalView, self).get_context_data(**kwargs)
		
		if self.request.GET.get('month'):
			month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
		else:
			today = datetime.today()
			month = date(today.year, today.month, 1)
		
		next_month = month + relativedelta(months=1)
		prev_month = month - relativedelta(months=1)
		context['prev_month'] = prev_month.strftime('%Y-%m-%d')
		context['next_month'] = next_month.strftime('%Y-%m-%d')
		context['year'] = month.year
		context['cur_month'] = month.strftime('%Y-%m-%d')
		context['month_verbose'] = month.strftime('%B')
		
		myear, mmonth = month.year, month.month
		number_of_days = monthrange(myear,mmonth)[1]
		context['month_header'] = [
			{'day': d, 'verbose': day_abbr[weekday(myear,mmonth,d)][:2]}
				for d in range(1, number_of_days+1)]
			
		if kwargs.get('pk'):
			queryset = [Student.objects.get(pk=kwargs['pk'])]
		else:
			current_group = get_current_group(self.request)
			if current_group:
				queryset = Student.objects.filter(student_group=current_group)
			else:
				queryset = Student.objects.all()
		
		order_by = self.request.GET.get('order_by', '')
		if order_by:
			queryset = queryset.order_by(order_by)
			if self.request.GET.get('reverse', '') == '1':
				queryset = queryset.reverse()
			
		update_url = reverse('journal') 
		
		students = []
		
		for student in queryset:
			try:
				journal = MonthJournal.objects.get(student=student, date=month)
			except:
				journal = None
			days = []
			for day in range(1,number_of_days+1):
				days.append({
					'day': day,
					'present': journal and getattr(journal, 'present_day%d' 
						% day, False) or False,
					'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
					'verbose_date': date(myear, mmonth, day).strftime('%w'),
					})
			students.append({
				'full_name': u'%s %s' % (student.first_name, student.last_name),
				'days': days,
				'id': student.id,
				'update_url': update_url,
				})
		
		context['pages'] = page_scroll(students, 10)
			
		page = int(self.request.GET.get('page', '1'))
		context['page'] = (page - 1) * 10
		if len(context['pages']) <= 1:
			context['students'] = students
		else:
			context['students'] = students[(page - 1)*10:page*10]
			
		return context
		
	def post(self, request, *args, **kwargs):
		data = request.POST
		current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
		month = date(current_date.year, current_date.month, 1)
		present = data['present'] and True or False
		student = Student.objects.get(pk=data['pk'])
		journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]
		
		setattr(journal, 'present_day%d' % current_date.day, present)
		journal.save()
		
		return JsonResponse({'status': 'success'})

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
