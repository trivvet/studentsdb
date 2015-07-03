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
	
	start = request.GET.get('start', '')
	end = request.GET.get('end', '')
	if start and end:
		students = students[start:end]
	else:
		students = students[0:3]
			
#	paginator = Paginator(students, 3)
#	page = request.GET.get('page')
#	try:
#		students = paginator.page(page)
#	except PageNotAnInteger:
#		students = paginator.page(1)
#	except EmptyPage:
#		students = paginator.page(paginator.num_pages)
	
	groups = Group.objects.all()
	return render(request, 'students/students_list.html', 
		{'students': students, 'groups': groups})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')
	
def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
	
def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
	
