# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.layout import Submit,  Div, Layout

from studentsdb.settings import ADMIN_EMAIL

from django.views.generic.edit import FormView

class ContactForm(forms.Form):
	def __init__(self, *args, **kwargs):
		# call original initializator
		super(ContactForm,self).__init__(*args,**kwargs)
		
		# this helper object allows us to customize form
		self.helper = FormHelper()
		
		# form tag attributes
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('contact_admin')
		
		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		
		# form buttons
		self.helper.layout = Layout(
			'from_email',
			'subject',
			'message',
			FormActions(
				Div('', css_class='col-sm-2'),
				Submit('send_button', u'Надіслати', css_class="btn btn-primary"),
				)
			)
	
	from_email = forms.EmailField(
		label=u"Ваша Email адреса")
		
	subject = forms.CharField(
		label=u"Заголовок листа",
		max_length=128)
		
	message = forms.CharField(
		label=u"Текст повідомлення",
		max_length=2560,
		widget=forms.Textarea)

class ContactView(FormView):
	template_name = 'contact_admin/contact_form.html'
	form_class = ContactForm
	success_url = '/contact-admin/'
	
	def form_valid(self, form):
		subject = form.cleaned_data['subject'] + '(' + form.cleaned_data['from_email'] + ')'
		message = form.cleaned_data['message']
		
		try: mail_admins(subject, message, 'trivvet@yahoo.com.ua')
		except Exception:
			messages.warning(self.request, u"Під час відправки листа виникла непередбачувана помилка. " \
				u"Спробуйте скористатися даною формою пізніше")
		else:
			messages.success(self.request, u'Повідомлення успішно надіслане')
		
		return super(ContactView, self).form_valid(form)


def contact_admin(request):
	# check if form was posted
	if request.method == "POST":
		# create a form instance
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			from_email = form.cleaned_data['from_email']
			
			try: send_mail(subject, message, from_email, [ADMIN_EMAIL])
			except Exception:
				messages.warning(request, u"Під час відправки листа виникла непередбачувана помилка. " \
					u"Спробуйте скористатися даною формою пізніше")
			else:
				messages.success(request, u'Повідомлення успішно надіслане')
				
			return HttpResponseRedirect(reverse('contact_admin'))
	else:
		form = ContactForm()
	
	return render(request, 'contact_admin/form.html', {'form': form})
