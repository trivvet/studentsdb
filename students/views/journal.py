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
		
	lists = []
	k = 1
	if Student_visiting.objects.count() % 3 == 0:
		counting = Student_visiting.objects.count() / 3
	else:
		counting = int(Student_visiting.objects.count() / 3) + 1
	for e in range(Student_visiting.objects.count())[::3]:
		lists.append(str(k))
		k = k + 1
	pages = {
		'lists': lists,
		'counting': counting
	}
	
	number_page = request.GET.get('page')
	if number_page:
		start = (int(number_page) - 1) * 3
		end = start + 3
		students = students[start:end]
	else:
		students = students[0:3]	
		
	days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)	
	
	groups = Group.objects.all()
	return render(request, 'students/journal_list.html', {'students': students, 'groups': groups, 'pages': pages, 'days': days})
