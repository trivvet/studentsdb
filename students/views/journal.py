# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.journal import Student_visiting
from ..models.groups import Group

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
