# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 15:35:02 2018

@author: Jacob
"""
import urllib.request
import urllib.parse
import http.cookiejar
#from PIL import Image
from json import loads
import chardet

header_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0','Connection':'keep-alive'}

#get请求
#txtmode={'leftTicketDTO.train_date':'2018-06-01','leftTicketDTO.from_station':'HCQ','leftTicketDTO.to_station':'XFN','purpose_codes':'ADULT'}
#get__mod = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-02-01&leftTicketDTO.from_station=HCQ&leftTicketDTO.to_station=XFN&purpose_codes=ADULT'

class Virtual_Long_Link():
    def __init__(self):
        self.cookie = http.cookiejar.CookieJar()
        #创建cookie处理器
        self.cookie_handler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookie_handler)
    def urlopen(self,url,params):
        params = urllib.parse.urlencode(params).encode('utf-8')
        req = urllib.request.Request(url,params,header_agent,method='POST')
        response = self.opener.open(req).read()
        return response
    
    def urlopen_str(self,url,params):
        params = urllib.parse.urlencode(params)
        url += '?' + params
        response = self.opener.open(url).read()
        return response
    
    def __test_cookie__(self):
        #声明一个CookieJar对象实例来保存cookie
        cookie = http.cookiejar.CookieJar()
        #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        handler= urllib.request.HTTPCookieProcessor(cookie)
        #通过CookieHandler创建opener
        opener = urllib.request.build_opener(handler)
        #此处的open方法打开网页
        response = opener.open('http://www.baidu.com')
        #打印cookie信息
        for item in cookie:
            print('Name = %s' % item.name)
            print('Value = %s' % item.value)
    
    def __save_cookie__(self):
        #保存cookies到文件，以便再次访问用
        #设置保存cookie的文件，同级目录下的cookie.txt
        filename = './pic/cookie.txt'
        #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        cookie = http.cookiejar.MozillaCookieJar(filename)
        #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        handler= urllib.request.HTTPCookieProcessor(cookie)
        #通过CookieHandler创建opener
        opener = urllib.request.build_opener(handler)
        #此处的open方法打开网页
        response = opener.open('http://www.baidu.com')
        #保存cookie到文件
        cookie.save(ignore_discard=True, ignore_expires=True)
    
    def __load_cookie__(self):
        filename = './pic/cookie.txt'
        #从文件加载cookies
        cookie = http.cookiejar.MozillaCookieJar()
        #从文件中读取cookie内容到变量
        cookie.load(filename, ignore_discard=True, ignore_expires=True)
        #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        handler= urllib.request.HTTPCookieProcessor(cookie)
        #通过CookieHandler创建opener
        opener = urllib.request.build_opener(handler)
        #此用opener的open方法打开网页
        response = opener.open('http://www.baidu.com')
        #打印信息
        print(response.read().decode('utf-8'))


#查询余票，不登陆也可进行
def query():
    params = {
            'leftTicketDTO.train_date':'2018-06-01',
            'leftTicketDTO.from_station':'WHN',
            'leftTicketDTO.to_station':'KMM',
            'purpose_codes':'ADULT'
            }
    url = 'https://kyfw.12306.cn/otn/leftTicket/query'
    response = vll.urlopen_str(url,params)
    dic = loads(response.decode())
    dic = dic['data']
    print('%6s%6s%6s%6s%6s%6s%6s%6s' % 
          ('车次','出发','结束','历时','软卧','无座','硬卧','硬座'))
    for it in dic['result']:
        list = it.split('|')
        print('%8s%8s%8s%8s%8s%8s%8s%8s' % 
              (list[3],list[8],list[9],list[10],list[23],list[26],list[28],list[29]))
        #软卧，无座，硬卧，硬座
        print(list[23],list[26],list[28],list[29])

#登陆
def login():
    #获取图片验证码
    img_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'
    data = {'login_site':'E',
            'module':'login',
            'rand':'sjrand'
            }
    response = vll.urlopen(img_url,data)
    with open ('./pic/img.jpg','wb') as f:
        f.write(response)
    
    #提交验证码
    pos_code = input("验证码位置:")
    code_list = pos_code.split(',')
    
    #图像重点的坐标
    pos_pic = ['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']
    sub = []
    for it in code_list:
        sub.append(pos_pic[int(it)])
    
    para = ','.join(sub)
    #具体见12306验证码验证过程
    check_url='https://kyfw.12306.cn/passport/captcha/captcha-check'
    data = {
            'login_site':'E',
            'rand':'sjrand',
            'answer':para
            }
    #post请求，验证验证码
    response = vll.urlopen(check_url,data)
    dic = loads(response.decode())
    print(dic)
    if(dic['result_code'] == '4'):
        print('验证码校验成功！！！')
    else:
        print('验证码校验错误！！！')
        return
    
    #验证码通过后验证账号密码
#    username  = input('账号:')·
#    passwd = input('密码:')
    data = {
            'username':'a649045636',
            'password':'fengzi1927',
            'appid':'otn'
            }
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    response = vll.urlopen(login_url,data)
    dic = loads(response.decode())
    if(dic['result_message'] == u'登录成功'):
        print('登陆成功！！！')
        return True
    return False

def get_passenger():
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    data = {'_json_att':'',
            'REPEAT_TOKEN':'934e64a695aceaf0d09428fc4d3823bf'
            }
    response = vll.urlopen(url,data)
    print(response.decode())
    
vll = Virtual_Long_Link()
if login():
    query()
#    for item in vll.cookie:
#        print(item)
    get_passenger()





#https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo
#_json_att	
#bed_level_order_num	000000000000000000000000000000
#cancel_flag	2
#oldPassengerStr	罗超元,1,420683199507120339,3_马秀兰,1,420683196906101529,1_
#passengerTicketStr	O,0,3,罗超元,1,420683199507120339,13995780812,N_O,0,1,马秀兰,1,420683196906101529,,N
#randCode	
#REPEAT_SUBMIT_TOKEN	c8124ea43143eede681334ff99c3a02e
#tour_flag	dc
#whatsSelect	1
