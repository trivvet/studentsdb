# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import datetime
from ..models.groups import Group
from ..models.exams import Exam
from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div
from crispy_forms.bootstrap import FormActions
from ..util import get_current_group
import pdb

# Views for Students

class ExamAddForm(ModelForm):
	class Meta:
		model = Exam
		fields = '__all__'
	
	def __init__(self, *args, **kwargs):
		super(ExamAddForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		
		self.helper.form_action = reverse('exams_add')
		
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

class ExamAddView(CreateView):
	template_name = 'students/exams_add.html'
	form_class = ExamAddForm
	success_url = 'exams'
	model = Exam
	
	def get_success_url(self):
		messages.success(self.request, u'Екзамен успішно додано')
		return reverse('exams')
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання екзамену відмінено')
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(ExamAddView, self).post(request, *args, **kwargs)


class ExamsUpdateForm(ModelForm):
	class Meta:
		model  = Exam
		fields = '__all__'
		
	def __init__(self, *args, **kwargs):
		super(ExamsUpdateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
        
		self.helper.form_action = reverse('exams_edit',
			kwargs={'pk': kwargs['instance'].id})
		self.helper.from_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		
		self.helper.help_text_inline = True
		self.helper.error_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4'
		self.helper.field_class = 'col-sm-8'

		self.helper.layout.append('')
		self.helper.layout[-1] = FormActions(
				Div('1', css_class='col-sm-4'),
				Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
				Submit('cancel_button', u'Скасувати', css_class='btn btn-link')
			)
        
class ExamsUpdateView(UpdateView):
	template_name = 'students/exams_edit_class.html'
	form_class = ExamsUpdateForm
	model  = Exam
	
	def get_success_url(self):
		messages.success(self.request, u"Екзамен успішно відредаговано!")
		return reverse('exams')
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u"Редагування екзамену відмінено")
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(ExamsUpdateView, self).post(request, *args, **kwargs)

def exams_list(request):
	current_group = get_current_group(request)
	if current_group:
		if Exam.objects.filter(group_exam=current_group):
			exams = Exam.objects.filter(group_exam=current_group)
		else:
			return render(request, 'students/exam_list.html', {})
	else:
		exams = Exam.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'matter', 'group_exam__title', 'time', 'teacher'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
	else:
		exams = exams.order_by('matter')
	
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
				messages.success(request, u"Екзамен %s успішно додано!" % matter)
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
