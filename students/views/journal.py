# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def journal_list(request):
	students = (
		{'id': 1,
		 'first_name': u'Вейдер',
		 'last_name': u'Дарт'},
		 {'id': 2,
		 'first_name': u'Мелфой',
		 'last_name': u'Люціус'},
		 {'id': 3,
		 'first_name': u'Бендер',
		 'last_name': u'Остап'}
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
	return render(request, 'students/journal_list.html', {'students': students, 'groups': groups})
