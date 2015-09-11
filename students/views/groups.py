# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.students import Student
from ..models.groups import Group
from django.views.generic import DeleteView, UpdateView, CreateView
from django.forms import ModelForm, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.layout import Submit, Layout, Div, Button
from django.contrib import messages
from ..util import get_current_group

class GroupAddForm(ModelForm):
	class Meta:
		model = Group
		fields = ['title', 'notes']
	
	def __init__(self, *args, **kwargs):
		super(GroupAddForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		
		self.helper.form_action = reverse('groups_add')
		
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

class GroupAddView(CreateView):
	template_name = 'students/groups_add.html'
	form_class = GroupAddForm
	success_url = 'groups'
	
	def get_success_url(self):
		messages.success(self.request, u'Групу успішно додано')
		return reverse('groups')
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання групи відмінено')
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(GroupAddView, self).post(request, *args, **kwargs)

class GroupUpdateForm(ModelForm):
	class Meta:
		model = Group
		fields = '__all__'
		
	def __init__(self, *args, **kwargs):
		super(GroupUpdateForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		
		self.helper.form_action = reverse('groups_edit',
			kwargs={'pk': kwargs['instance'].id})
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control-label'
		self.helper.field_class = 'col-sm-8'
		
		self.helper.layout.append('')
		self.helper.layout[-1] = FormActions(
			Div('', css_class='col-sm-4'),
			Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
			)

class GroupUpdateView(UpdateView):
	model = Group
	template_name = 'students/groups_edit_class.html'
	form_class = GroupUpdateForm
	success_url = 'groups'
	
	def get_success_url(self):
		messages.success(self.request, u'Групу успішно змінено')
		return reverse('groups')
		
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(request, u'Редагування групи відмінено')
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(GroupUpdateView, self).post(request, *args, **kwargs)

class GroupDeleteView(DeleteView):
	model = Group
	template_name = 'students/groups_confirm_delete.html'
	
	def get_success_url(self):
		messages.success(self.request, u'Групу видалено успішно')
		return reverse('groups')
	
	def post(self, request, pk, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(self.request, u'Видалення групи відмінено!')
			return HttpResponseRedirect(reverse('groups'))
		elif Student.objects.filter(student_group=Group.objects.get(pk=pk)):
			messages.error(self.request, u"Видалення неможливе, в групі присутні студенти")
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(GroupDeleteView, self).post(request, *args, **kwargs)	

# Group list		
def groups_list(request):
	current_group = get_current_group(request)
	if current_group:
		groups = Group.objects.filter(pk=current_group.id)
	else:	
		groups = Group.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'title', 'leader__first_name'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			groups = groups.reverse()
	else:
		groups = groups.order_by('title')
	
	pages = []
	k = 0
	if not int(groups.count() % 3) == 0:
		k = 1
	for i in range(groups.count() / 3 + k):
		pages.append(str(i+1))
		
	number_page = int(request.GET.get('page', '1'))
	if number_page > len(pages):
		number_page = len(pages)
	groups = groups[number_page * 3 - 3:number_page * 3]
	
	return render(request, 'students/groups_list.html', {'groups': groups, 'pages': pages})

# Adding group's form
def groups_add(request):
	
	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			data = {'notes': request.POST.get('notes')}
			errors = {}
			
			if not request.POST.get('title', '').split():
				errors['title'] = u"Назва групи є обов’язковою"
			else:	
				simple_groups = Group.objects.filter(title=request.POST.get('title'))
				if len(simple_groups) > 0:
					errors['title'] = u'Група з назвою "%s" вже існує' % request.POST.get('title')
				else:
					data['title'] = request.POST.get('title')
			if not errors:
				groups = Group(**data)
				groups.save()
				messages.success(request, u'Групу %s додано!' % request.POST['title'])
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, u'Будь-ласка виправте наступні помилки')
				return render(request, 'students/groups_add.html', {'errors': errors})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання групи відмінено')
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_add.html', {})

# Edit group's form	
def groups_edit(request, pk):
	errors = {}
	students = Student.objects.filter(student_group=pk)
	group = Group.objects.filter(id=pk)
	if len(students) < 1:
		errors['leader'] = u"В групі немає жодного студента"
	if request.method == 'POST':
		if request.POST.get('add_button') is not None:
			data = {'title': request.POST.get('title'), 'notes': request.POST.get('notes')}
			if request.POST.get('leader'):
				k = len(Group.objects.filter(leader=request.POST.get('leader')))
				if k == 0 or Group.objects.get(leader=request.POST.get('leader')) == Group.objects.get(pk=pk):
					u = 'yes'
					data['leader'] = Student.objects.get(pk=request.POST.get('leader'))
				else:
					errors['leader'] = u"Даний студент є старостою іншої групи"
			data['id'] = pk
			if errors:
				leader = Student.objects.get(pk=request.POST.get('leader'))
				messages.error(request, u"Будь-ласка виправте наступні помилки")
				return render(request, 'students/groups_edit.html', 
					{'errors':errors, 'students':students, 'leader':leader})
			else:
				groups = Group(**data)
				groups.save()
				messages.success(request, u"Група %s успішно змінена" % request.POST.get('title'))
				return HttpResponseRedirect(reverse('groups'))
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Редагування групи відмінено")
			return HttpResponseRedirect(reverse('groups'))
	else:
		group = Group.objects.get(id=pk)
		return render(request, 'students/groups_edit.html', {'group':group, 'errors':errors, 'students':students})
	
def groups_delete(request, pk):
	if request.method == "POST":
		if request.POST.get('delete_button') is not None:
			if Student.objects.filter(student_group=Group.objects.get(pk=pk)):
				messages.error(request, u"Видалення неможливе, в групі присутні студенти")
			else:
				messages.success(request, u"Група %s успішно видалена!" % Group.objects.get(pk=pk))
				group_delete = Group.objects.get(pk=pk)
				group_delete.delete()
			return HttpResponseRedirect(reverse('groups'))
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u"Видалення групи відмінено")
			return HttpResponseRedirect(reverse('groups'))
	else:
		group = Group.objects.get(id=pk)
		return render(request, 'students/groups_delete.html', {'group': group})
	
