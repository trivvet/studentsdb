# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import datetime
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
	
	pages = []
	k = 0
	if not int(exams.count() % 5) == 0:
		k = 1
	for i in range(int(exams.count() / 5) + k):
		pages.append(str(i+1))

	number_page = int(request.GET.get('page', '1'))
	if number_page > len(pages):
		number_page = len(pages)
	exams = exams[number_page * 5 - 5:number_page * 5]
	groups = Group.objects.all()
	return render(request, 'students/exam_list.html', 
		{'exams': exams, 'groups': groups, 'pages': pages})
		
def exams_add(request):
	groups = Group.objects.all()
	
	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			data = {}
			errors = {}
			
			matter = request.POST.get('matter', '').strip()
			if not matter:
				errors['matter'] = u'Назва предмету є обов’язковою'
			else:
				data['matter'] = matter
				
			time = request.POST.get('time', '').strip() + ':00'
			if not time:
				errors['time'] = u'Дата є обов’язковою'
			else:
				try:
					datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
				except Exception:
					errors['time'] = u'Введіть коректний формат дати і часу (напр. 2015-10-01 10:00)'
				else:
					data['time'] = time
			
			teacher = request.POST.get('teacher', '').strip()
			if not teacher:
				errors['teacher'] = u'Прізвище вчителя є обов’язковим'
			else:
				data['teacher'] = teacher
				
			group_exam = request.POST.get('group_exam', '')
			if not group_exam:
				errors['group_exam'] = u'Оберіть групу для екзамену'
			elif len(Group.objects.filter(pk=group_exam)) > 1:
				errors['group_exam'] = u'Оберіть конкретну %s групу' % group_exam
			else:
				data['group_exam'] = Group.objects.get(pk=group_exam)
				
			if not errors:
				exam = Exam(**data)
				exam.save()
				messages.success(request, u"Екзамен успішно додано!")
				return HttpResponseRedirect(reverse('exams'))
			else:
				return render(request, 'students/exams_add.html', {'groups': groups, 'errors': errors})
				
		elif request.POST.get('close_button') is not None:
			messages.info(request, u"Додавання екзамену відмінено!")
			return HttpResponseRedirect(reverse('exams'))
	else:
		return render(request, 'students/exams_add.html', {'groups': groups})
	
def exams_edit(request, pk):
	groups = Group.objects.order_by('title')	
	
	if request.method == "POST":
		if request.POST.get('save_button') is not None:
			data = {'id': pk}
			errors = {}
			
			matter = request.POST.get('matter', '').strip()
			if not matter:
				errors['matter'] = u'Назва предмету є обов’язковою'
			else:
				data['matter'] = matter
				
			time = request.POST.get('time', '').strip() + ':00'
			if not time:
				errors['time'] = u'Дата є обов’язковою'
			else:
				try:
					datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
				except Exception:
					errors['time'] = u'Введіть коректний формат дати і часу (напр. 2015-10-01 10:00)'
				else:
					data['time'] = time
			
			teacher = request.POST.get('teacher', '').strip()
			if not teacher:
				errors['teacher'] = u'Прізвище вчителя є обов’язковим'
			else:
				data['teacher'] = teacher
				
			group_exam = request.POST.get('group_exam', '')
			if not group_exam:
				errors['group_exam'] = u'Оберіть групу для екзамену'
			elif len(Group.objects.filter(pk=group_exam)) > 1:
				errors['group_exam'] = u'Оберіть конкретну %s групу' % group_exam
			else:
				data['group_exam'] = Group.objects.get(pk=group_exam)
			
			if not errors:
				exam = Exam(**data)
				exam.save()
				messages.success(request, u"Екзамен успішно змінено!")
				return HttpResponseRedirect(reverse('exams'))
			else:
				group_exam = Group.objects.get(pk=request.POST.get('group_exam'))
				return render(request, 'students/exams_edit.html', {'groups': groups, \
					'errors': errors, 'group_exam': group_exam})
				
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Редагування екзамену відмінено!")
			return HttpResponseRedirect(reverse('exams'))	
	else:
		exam = Exam.objects.get(pk=pk)
		return render(request, "students/exams_edit.html", {'exam': exam, 'groups': groups})
		
def exams_delete(request, pk):
	exam = Exam.objects.get(pk=pk)
	
	if request.method == "POST":
		if request.POST.get('delete_button') is not None:
			exam.delete()
			messages.success(request, u"Екзамен %s успішено видалений!" % exam.matter)
			return HttpResponseRedirect(reverse('exams'))
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Видалення екзамена відмінено!")
			return HttpResponseRedirect(reverse('exams'))
	else:
		return render(request, 'students/exams_delete.html', {'exam': exam})
