# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

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
	
