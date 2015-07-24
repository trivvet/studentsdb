# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..models.students import Student
from ..models.groups import Group
from datetime import datetime
from PIL import Image

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
	if Student.objects.count() % 3 == 0:
		counting = Student.objects.count() / 3
	else:
		counting = int(Student.objects.count() / 3) + 1
	for e in range(Student.objects.count())[::3]:
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
	
	groups = Group.objects.all()
	return render(request, 'students/students_list.html', 
		{'students': students, 'groups': groups, 'pages': pages})

def students_add(request):
	groups = Group.objects.all().order_by('title')
	# was form posted:
	if request.method == "POST":
		# was form add button clicked:
		if request.POST.get('add_button') is not None:
			# errors collection
			errors = {}
			# validate student data will go here
			data = {'middle_name': request.POST.get('middle_name'),
				'notes': request.POST.get('notes')}
			# validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Прізвище є обов’язковим"
			else:
				data['first_name'] = first_name
				
			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Ім’я є обов’язковим"
			else:
				data['last_name'] = last_name
				
			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов’язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
				else:
					data['birthday'] = birthday
				
			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білету є обов’язковим"
			else:
				data['ticket'] = ticket
				
			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберiть групу для студента"
			else:
				if len(Group.objects.filter(pk=student_group)) != 1:
					errors['student_group'] = u"Оберіть конкретну групу"
				else:
					data['student_group'] = Group.objects.get(pk=student_group)
				
			photo = request.FILES.get('photo')
			if photo:
				try: 
					Image.open(photo).verify()
				except: 
					errors['photo'] = u"Оберіть файл зображення"
				
				if not photo.size < 2097152:
					errors['photo'] = u"Оберіть файл розміром до 2МБ"
				else:
					data['photo'] = photo
				
			# Якщо дані були введені коректно:
			if not errors:
				# save student
				student = Student(**data)
				student.save()
				# Повертаємо користувача до списку студентів
				messages.success(request, u"Студент %s %s успішно доданий!" 
				% (data['first_name'], data['last_name']))
				return HttpResponseRedirect(reverse('home'))
			else:
			# Якщо дані були введені некоректно:
				# Віддаємо шаблон форми разом із знайденими помилками
				return render(request, 'students/students_add.html', 
					{'groups': groups, 'errors': errors})
		# Якщо кнопка скасування була натиснута:	
		elif request.POST.get('cancel_button') is not None:
			# Повертаємо користувача до списку студентів
			messages.info(request, u"Додавання студента скасовано!")
			return HttpResponseRedirect(reverse('home'))	
	# Якщо форма не була запощена:
	else:
		# Повертаємо код початкового стану форми
		return render(request, 'students/students_add.html', 
			{'groups': groups})
	
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
	
