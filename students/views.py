# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students

def students_list(request):
	students = (
		{'id': 1,
		 'first_name': u'Вейдер',
		 'last_name': u'Дарт',
		 'ticket': 27,
		 'image': 'img/SOS.JPG'},
		 {'id': 2,
		 'first_name': u'Мелфой',
		 'last_name': u'Люціус',
		 'ticket': 618,
		 'image': 'img/Mich.JPG'},
		 {'id': 3,
		 'first_name': u'Бендер',
		 'last_name': u'Остап',
		 'ticket': 411,
		 'image': 'img/Kir.JPG'},
	)
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
	
# Views for Groups

def groups_list(request):
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
	return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')
	
def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)
	
def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)
	
# Views for Journal

def journal_list(request):
	return HttpResponse('<h1>Journal</h1>')
