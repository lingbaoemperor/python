from django.http import HttpResponse
from django.shortcuts import render_to_response

def search_form(req):
	return render_to_response('search-form.html')
def search(req):
	req.encoding='utf-8'
	if 'q' in req.GET:
		message = '你搜索的内容为：'+req.GET['q']
	else:
		message = '你提交了空表单'
	return HttpResponse(message)
