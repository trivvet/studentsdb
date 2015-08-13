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
		messages.info(self.request, u'Групу видалено успішно')
		return reverse('groups')
	
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(self.request, u'Редагування групи відмінено!')
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(GroupDeleteView, self).post(request, *args, **kwargs)	
		
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
				return render(request, 'students/groups_add.html', {'errors': errors})
		elif request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання групи відмінено')
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_add.html', {})
	
def groups_edit(request, pk):
	if request.method == 'POST':
		return HttpResponseRedirect(reverse('groups'))
	else:
		group = Group.objects.get(id=pk)
		return render(request, 'students/groups_edit.html', {'group':group})
	
def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)
	
