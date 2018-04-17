from django.http import HttpResponse
from django.shortcuts import render

def hello(req):
	#return render(req,'hello.html',{'hello':'Hello World'})
	return render(req,'hello.html')

def main(req):
	return HttpResponse('<hl>This is main page!!!</hl>')
