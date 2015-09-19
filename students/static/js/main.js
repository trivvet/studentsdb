var hrefFirst;

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
	$('#id_birthday').wrap("<div class='input-group date' id='div_id_birthday'>\
		</div>").after("<span class='input-group-addon'>\
	   <span class='glyphicon glyphicon-calendar'></span></span>");
	$('#id_birthday').datetimepicker({
		'format': 'YYYY-MM-DD'
	}).on('dp.hide', function(event) {
		$(this).blur();
	});
	$('#id_time').datetimepicker({
		'format': 'YYYY-MM-DD HH:mm'
	}).on('dp.hide', function(event) {
		$(this).blur();
	});
}

function readURL(input) {
	var reader = new FileReader()
	reader.onload = function(e) {
		$(input).after('<img src="' + e.target.result + '" heigth="90" width="90">');
	};
	reader.readAsDataURL(input.files[0]);
}

function initAddImage() {
	$('#id_photo').change(function(event) {
		readURL(this);
	});
}

function initEditImage() {
	var link = $('#div_id_photo div a').attr('href');
	console.log(link);
	$('#div_id_photo div br').before('<img src="' + 
		link + '" heigth="90" width="90">');
}

function initForm(form, modal) {
	initDateFields();
//	$('#id_notes').removeAttr('rows');

	initAddImage();
	initEditImage();
	
	form.find('input[name="cancel_button"]').click(function(event) {
		modal.modal('hide');
		return false;
	});
	
	form.ajaxForm({
		'dataType': 'html',
		'beforeSend': function(xhr, settings) {
			$('#progress').modal({'keyboard': false, 'backdrop': false, 'show':true});
			$('.progress-bar').animate({width: '100%'}, 'slow');
		},
		'error': function() {
			$('#progress').modal('hide');
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше!');
			return false;
		},
		'success': function(data, status, xhr) {
			$('#progress').modal('hide');
			var html = $(data), newform = html.find('#content-columns form');
			modal.find('.modal-body').html(html.find('.alert'));
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);
				initEditStudentForm(newform, modal);
			} else {
				modal.find('.modal-footer').hide('fast');
				modal.find('.modal-body').show('fast');
				modal.modal({'keyboard': false, 'backdrop': false, 'show':true});
				var page = html.find('#page');
				$('#proba').html(page);
				setTimeout(function(){modal.modal('hide');}, 800);
				
				initEditPage();
				initJournal();
				initPaginator();
				initSorting()
			}
		}
	}); 
	return false;
}; 

function initEditPage() {
	$('a.form-link').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'beforeSend': function(xhr, settings) {
				$('#progress').modal({'keyboard': false, 'backdrop': false, 'show':true});
				$('.progress-bar').animate({width: '100%'}, 'slow');
			},
			'success': function(data, status, xhr) {
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
					return false;
				}
				var modal = $('#myModal'), html = $(data), 
				form = html.find('#content-columns form');
				modal.find('.modal-title').html(html.find('#content-columns h2').text());
				modal.find('.modal-body').html(form);
				modal.find('.modal-footer').hide();
				$('div.dropdown').removeClass('open');

				initForm(form, modal);
				
				$('#progress').modal('hide');
				modal.modal({'keyboard': false, 'backdrop': false, 'show':true});
				
			},
			'error': function() {
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
				return false;
			}
		});
		
		return false;
	});
}

function initPageSelector() {
	$('a.page_change').click(function(event) {
		var link = $(this);
		$('li.active').removeClass('active');
		link.parent().addClass('active');
		link.blur();
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr) {
				var html = $(data), page = html.find('#page');
				$('#proba').html(page);
				$('h2.head').html(html.find('.title_page'));
				
				var hrefFirst;
				
				initEditPage();
				initJournal();
				initPaginator();
				initSorting()
				
			},
			'error': function() {
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
				return false;
			}
		});
		
		return false;
	});
}

function initPaginator () {
	$('a.paginator').click(function(event) {
		var link = $(this);
		$('.pagination li.active').removeClass('active');
		if (link.hasClass('arrBack')) {
			$('.pagination li:nth-child(2)').addClass('active');
		} else if (link.hasClass('arrForward')){
			$('.pagination li:nth-last-child(2)').addClass('active');
		} else {
			link.parent().addClass('active');
		};
		link.blur();
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr) {
				var html = $(data), page = html.find('tbody').html();
				$('tbody').html(page);
				
				initEditPage();
				initJournal();
				
			},
			'error': function() {
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
				return false;
			}
		});
		
		return false;
	});
}

function initSorting() {
	$('a.sorting').click(function(event) {
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr) {
				var html = $(data), page = html.find('tbody').html();
				$('tbody').html(page);
				if (link.hasClass('reverse')) {
					link.attr('href', link.attr('href') + '&amp;reverse=1');
					link.removeClass('reverse');
					link.addClass('direct');
					link.children('span.arrUp').show();
					link.children('span.arrDown').hide();
				} else if (link.hasClass('direct')) {
					console.log(hrefFirst);
					link.attr('href', hrefFirst);
					link.removeClass('direct');
					link.addClass('reverse');
					link.children('span.arrUp').hide();
					link.children('span.arrDown').show();
				} else {
					if (hrefFirst) {
						$('a.direct').removeClass('direct').attr('href', hrefFirst);
						$('a.reverse').removeClass('reverse').attr('href', hrefFirst);
					};
					hrefFirst = link.attr('href');
					console.log(hrefFirst);
					link.attr('href', link.attr('href') + '&amp;reverse=1');
					link.addClass('direct');
					$('span.arrUp').hide();
					$('span.arrDown').hide();
					link.children('span.arrUp').show();
				};
//				link.attr('href', 	
				
				initEditPage();
				initJournal();
				initPaginator();
				
			},
			'error': function() {
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
				return false;
			}
		});
		
		return false;
	});
}

$(document).ready(function() {
	
	initJournal();
	initGroupSelector();
	initDateFields();
	initEditPage();
	initPageSelector();
	initPaginator();
	initSorting();
});
