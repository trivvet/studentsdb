def page_scroll(list_smt, n):
	pages = []
	k = 0
	if len(list_smt) % n == 0:
		k = len(list_smt) / n
	else:
		k = len(list_smt) / n + 1
	for page in range(k):
		pages.append(str(page+1))
	return pages
