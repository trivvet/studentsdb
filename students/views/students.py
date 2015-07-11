# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Student, Group

# Views for Students

def students_list(request):
	
	students = Student.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
		students = students.order_by('first_name')
	
	
	lists = []
	k = 1
	for e in range(Student.objects.count())[::3]:
		lists.append(str(k))
		k = k + 1
	pages = {
		'lists': lists,
		'counting': Student.objects.count()
	}
	
	number_page = request.GET.get('page', '')
	if number_page:
		start = (int(number_page) - 1) * 3
		end = start + 3
		students = students[start:end]
	else:
		students = students[0:3]
	
	groups = Group.objects.all()
	return render(request, 'students/students_list.html', 
		{'students': students, 'groups': groups, 'pages': pages})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')
	
def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
	
def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
	
#	paginator = Paginator(students, 3)
#	page = request.GET.get('page')
#	try:
#		students = paginator.page(page)
#	except PageNotAnInteger:
#		students = paginator.page(1)
#	except EmptyPage:
#		students = paginator.page(paginator.num_pages)
	
