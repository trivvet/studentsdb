def students_proc(request):
	return {'PORTAL_URL': 'http://' + request.META['HTTP_HOST'] }
