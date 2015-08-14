# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..models.groups import Group
from ..models.exams import Exam

# Views for Students
def exams_list(request):
	exams = Exam.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'matter', 'group_exam__title', 'time', 'teacher'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
	else:
		exams = exams.order_by('id')
	
	groups = Group.objects.all()
	return render(request, 'students/exam_list.html', 
		{'exams': exams, 'groups': groups})
		
def exams_add(request):
	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			data = {}
			errors = {}
			
			messages.success(request, u"Екзамен додано!")
			return HttpResponseRedirect(reverse('exams'))
		elif request.POST.get('close_button') is not None:
			messages.info(request, u"Додавання екзамену відмінено!")
			return HttpResponseRedirect(reverse('exams'))
	else:
		groups = Group.objects.all()
		return render(request, 'students/exams_add.html', {'groups': groups})
	
def exams_edit(request, sid):
	return HttpResponse('<h1>Edit Exam %s</h1>' % sid)
	
def exams_delete(request, sid):
	return HttpResponse('<h1>Delete Exam %s<h1>' % sid)
