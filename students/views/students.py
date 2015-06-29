# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models import Student

# Views for Students

def students_list(request):
	students = Student.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
			
	groups = (
		{'id': 1,
		 'name': u'1Б-04',
		 'leader': {'id': 4, 'name': u'Бацура Олександр'}},
		{'id': 2,
		 'name': u'2Б-04',
		 'leader': {'id': 5, 'name': u'Козаченко Богдан'}},
		{'id': 3,
		 'name': u'БМ-04',
		 'leader': {'id': 2, 'name': u'Люціус Мелфой'}},
		 )
	return render(request, 'students/students_list.html', 
		{'students': students, 'groups': groups})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')
	
def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
	
def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
	
