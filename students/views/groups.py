# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
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
	return HttpResponse('<h1>Group Add Form</h1>')
	
def groups_edit(request, pk):
	return HttpResponse('<h1>Edit Group %s</h1>' % pk)
	
def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)
	
