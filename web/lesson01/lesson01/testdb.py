from django.http import HttpResponse
from testmodel.models import Test

def testdb(req):
	return HttpResponse('<p>test database!</p>')

def add(req):
	test1 = Test(name='rubobb')
	test1.save()
	return HttpResponse('<p>success to adding data!!!</p>')
def get(req):
	#获得所有数据行,select *
	response = ""
	list = Test.objects.all()
	#条件,where
	Test.objects.filter(id=1)
	#单个对象
	response1 = Test.objects.get(id=1)
	#限制返回的数据
	Test.objects.order_by('name')[0:2]
	#排序
	Test.objects.order_by('id')
	#以上方法同时使用
	Test.objects.filter(name="runoob").order_by('id')
	#输出
	for var in list:
		response += var.name + ' '
	return HttpResponse('<p>'+response+'</p>')

def update(req):
	#修改id = 1的name字段再保存
	test = Test.objects.get(id=1)
	test.name = 'Google'
	test.save()
	
	#或者
	#Test.objects.filter(id=1).update(name='Google')
	#Test.objects.all().update(name='Google')
	return HttpResponse('<p>success to updating!!!</p>')

def delete(req):
	test = Test.objects.get(id=1)
	test.delete()
	
	#或者
	#Test.objects.filter(id=1).delete()
	#Test.objects.all().delete()
	return HttpResponse('<p>success to delete!!!</p>')
