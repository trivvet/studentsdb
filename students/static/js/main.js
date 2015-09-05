function initJournal() {
	var indicator = $('#ajax-progress-indicator');
	var problem = $('#error');
	
	$('.day-box input[type="checkbox"]').click(function(event) {
		var box = $(this);
		$.ajax(box.data('url'), {
			'type': 'POST',
			'async': true,
			'dataType': 'json',
			'data': {
				'pk': box.data('student-id'),
				'date': box.data('date'),
				'present': box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			'beforeSend': function(xhr, settings) {
				indicator.show()
			},
			'error': function(xhr, status, error) {
				problem.append(error);
				problem.show();
				alert(error);
				indicator.hide();
			},
			'success': function(data, status, xhr) {
				indicator.hide();
			}
		});
	});
};

function initGroupSelector() {
	$('#group-selector select').change(function(event) {
		var group = $(this).val();
		if (group) {
			Cookies.set('current_group', group, {'path': '/', 'expires': 365});
		} else {
			Cookies.remove('current_group', {'path': '/'});
		};
		location.reload(true);
		return true;
	});
};

function initDateFields() {
	$('#id_birthday').datetimepicker({
		'format': 'YYYY-MM-DD'
	}).on('dp.hide', function(event) {
		$(this).blur();
	});
	$('#datetimeinput').datetimepicker({
		'format': 'YYYY-MM-DD HH-mm',
	}).on('dp.hide', function(event) {
		$(this).blur();
	});
};

function initEditStudentForm(form, modal) {
	initDateFields();
	
	form.find('input[name="cancel_button"]').click(function(event) {
		modal.modal('hide');
		return false;
	});  
	
	form.ajaxForm({
		'dataType': 'html',
		'error': function() {
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше!');
			return false;
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-columns form');
			modal.find('.modal-body').html(html.find('.alert'));
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);
				initEditStudentForm(newform, modal);
			} else {
				modal.find('.modal-footer').show('fast');
				$('.progress-bar').animate({width: '100%'}, 'slow');
				setTimeout(function(){location.reload(true);}, 500);
				modal.modal({'keyboard': false, 'backdrop': false, 'show':true});
			}
		}
	}); 
	return true;
}; 

function initEditStudentPage() {
	$('a.student-edit-form-link').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr) {
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь ласка пізніше');
					return false;
				}
				
				var modal = $('#myModal'), html = $(data), 
				form = html.find('#content-columns form');
				modal.find('.modal-title').html(html.find('#content-columns h2').text());
				modal.find('.modal-body').html(form);
				modal.find('.modal-footer').hide()
				
				initEditStudentForm(form, modal);
				
				modal.modal({'keyboard': false, 'backdrop': false, 'show':true});
			},
			'error': function() {
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
				return false;
			}
		});
		
		return false;
	});
};	

$(document).ready(function() {
	initJournal();
	initGroupSelector();
	initDateFields();
	initEditStudentPage();
});
