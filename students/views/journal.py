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
	return render(request, 'students/journal_list.html', {'students': students})
