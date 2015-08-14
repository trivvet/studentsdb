# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.students import Student
from ..models.groups import Group
from django.views.generic import DeleteView
from django.contrib import messages

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
	groups = Group.objects.all()
	
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'title', 'leader__first_name'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			groups = groups.reverse()
	else:
		groups = groups.order_by('title')
	
	lists = []
	k = 1
	if Group.objects.count() % 3 == 0:
		counting = Group.objects.count() / 3
	else:
		counting = int(Group.objects.count() / 3) + 1
	for e in range(Group.objects.count())[::3]:
		lists.append(str(k))
		k = k + 1
	pages = {
		'lists': lists,
		'counting': counting
	}
	
	number_page = request.GET.get('page', '')
	if number_page:
		start = (int(number_page) - 1) * 3
		end = start + 3
		groups = groups[start:end]
	else:
		groups = groups[0:3]
	
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
	
