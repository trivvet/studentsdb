# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..models.students import Student
from ..models.groups import Group
from ..views.paginator import page_scroll
from django import forms
from django.forms import ModelForm, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.layout import Submit, Layout, Div, Button, Field
from datetime import datetime
from ..util import get_current_group
from PIL import Image
import pdb, time

# Views for Students

class StudentAddForm(ModelForm):
	class Meta:
		model = Student
		fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 
			'ticket', 'student_group', 'notes']
		widgets = {
			'notes': forms.Textarea(attrs={'rows':4, 'cols':40}),
			}
		
	def __init__(self, *args, **kwargs):
		super(StudentAddForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		
		self.helper.form_action = reverse('students_add')
		
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control-label'
		self.helper.field_class = 'col-sm-8'
		
		self.helper.layout.append('')
		self.helper.layout[-1] = FormActions(
			Div('', css_class='col-sm-4'),
			Submit('add_button', u'Додати', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
			)

class StudentAddView(CreateView):
	template_name = 'students/students_add.html'
	form_class = StudentAddForm
	success_url = 'home'
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(self.request, u'Додавання студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentAddView, self).post(request, *args, **kwargs)
	
	def get_success_url(self):
		messages.success(self.request, u'Студент успішно доданий')
		return reverse('home')
		


class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 
			'ticket', 'student_group', 'notes']
		widgets = {
			'notes': forms.Textarea(attrs={'rows':4, 'cols':40}),
			}
		
	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		
		# form tag attributes
		self.helper.form_action = reverse('students_edit',
			kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		
		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control-label'
		self.helper.field_class = 'col-sm-8'
		
		# form buttons
		self.helper.layout.append('')
		self.helper.layout[-1] = FormActions(
			Div('', css_class='col-sm-4'),
			Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
			)
			
class StudentUpdateView(UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentUpdateForm
	
	def get_success_url(self):
		messages.success(self.request, u'Дані студента успішно змінено!')
		return reverse('home')
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(self.request, u'Редагування студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			time.sleep(2)
			return super(StudentUpdateView, self).post(request, *args, **kwargs)
			
	def get_context_data(self, **kwargs):
		context = super(StudentUpdateView, self).get_context_data(**kwargs)
		time.sleep(2)
		return context


class StudentDeleteView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_delete.html'
	form_class = StudentUpdateForm
	
	def get_success_url(self):
		messages.success(self.request, u'Студента успішно видалено')
		return reverse('home')
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(self.request, u'Видалення студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentDeleteView, self).post(request, *args, **kwargs)

def students_list(request):
	
	current_group = get_current_group(request)
	if current_group:
		students = Student.objects.filter(student_group=current_group)
	else:
		students = Student.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'last_name', 'first_name', 'ticket', 'student_group__title'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
		students = students.order_by('first_name')
	
	pages = page_scroll(students, 3)
		
	number_page = int(request.GET.get('page', '1'))
	if number_page > len(pages):
		number_page = len(pages)
	if number_page > 0:
		students = students[number_page * 3 - 3: number_page * 3]
	
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
				else:
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
				messages.error(request, u"Будь-ласка виправте наступні помилки")
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
	
# def students_edit(request, pk):
#	return render(request, 'students/students_edit.html', {})
	
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
	
