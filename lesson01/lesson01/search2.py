from django.shortcuts import  render
from django.views.decorators import csrf

def search_post(req):
	ctx = {}
	print(req.POST)
	if req.POST:
		ctx['rlt'] = req.POST['q']
	return render(req,"post.html",ctx)
