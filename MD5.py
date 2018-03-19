# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 14:00:26 2018

MD5

@author: chaoyuan
"""
import math
import socket

#返回128为的结果，整型
def encrypt(raw_string):        
    byte_str = raw_string.encode('utf8')
    _init(byte_str)
    _prepare(byte_str)
    _start_loop()
    return _merge()

#初始化
def _init(string):
    #链接变量
    global c_v
    #轮数
    global circles
    #分组个数
    global groups
    #每组子分组数
    global items
    #分组最小单元
    global item_list
    #加法项常量
    global const_list
    
    c_v = [0x67452301,0xefcdab89,0x98badcfe,0x10325476]
    circles = 4
    items = 16
    
    str_len = len(string)
    #分组个数，每组512位即64字节，留八字节填充，剩余不足八字则增加一个分组
    groups = (str_len//64)+1
    if((str_len%64) > 56):
        groups += 1
    #分组最小单元用矩阵存储，groups*item个
    item_list = [[0]*items for i in range(groups)]
    #加法项常量，一大轮64次，共64个
    const_list = [0]*(items*circles)
    #加法常量:abs(sin(i))乘以2的32次方取整
    for i in range(items*circles):
        const_list[i] = math.floor((2**32)*abs(math.sin(i+1)))
    
#分割数据
def _prepare(byte_str):
    global item_list
    string_len = len(byte_str)
    string_index = 0
    row = 0
    col = 0
    #一组为一行(16个)
    while (string_index+4) <= string_len:
        item_list[row][col] = (item_list[row][col]<<8)+byte_str[string_index+3]
        item_list[row][col] = (item_list[row][col]<<8)+byte_str[string_index+2]
        item_list[row][col] = (item_list[row][col]<<8)+byte_str[string_index+1]
        item_list[row][col] = (item_list[row][col]<<8)+byte_str[string_index]
        string_index += 4
        col += 1
        if(col == 16):
            row += 1
            col = 0
            
    #最后补充1bit 1
    #若有且不足4字节的部分
    last  = string_len - string_index
    if last:
        item_list[row][col] = (item_list[row][col]<<8)+0x80
        for i in range(last):
            item_list[row][col] = (item_list[row][col]<<8)+byte_str[string_index+i]
    #无剩余
    else:
        item_list[row][col] = item_list[row][col]+0x80
    
    #最后64位(8字节填充消息长度)
    string_len *= 8
    item_list[-1][-2] = string_len&0xffffffff
    item_list[-1][-1] = (string_len&0xffffffff00000000)>>32

def _start_loop():
    global c_v
    global const_list
    global item_list
    global groups
    global circles
    fun_list = [(lambda x,y,z : ((x&y)|((~x)&z))),
                (lambda x,y,z : ((x&z)|(y&(~z)))),
                (lambda x,y,z : (x^y^z)),
                (lambda x,y,z : (y^(x|(~z))))]
    #向左环移
    shift = (lambda x,n : ((x<<n)|(x>>(32-n))))
    #[A,B,C,D]赋值给temp
    temp = c_v[:]
    #每小轮16次，[a,b,c,d]顺序4次一循环
    orders = [[0,1,2,3],
             [3,0,1,2],
             [2,3,0,1],
             [1,2,3,0]]
    #环移量也是4次一循环
    offset_matrix = [[7,12,17,22],
                     [5,9,14,20],
                     [4,11,16,23],
                     [6,10,15,21]]
    #16次最小分组单元的顺序（加）
    group_order = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                   [1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12],
                   [5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2],
                   [0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]]
    #循环groups次
    for i in range(groups):
        temp = c_v[:]
        #4轮
        for j in range(circles):
            offset = offset_matrix[j]
            #每轮16次，4乘4
            for k in range(4):
                for l in range(4):
                    #每次[a,b,c,d]中的其中3个做一次非线性运算，然后加上第四个变量、文本的一个子分组（最小分组）和一个常量
                    #在将所得结果环移一个不定的数，并加上[a,b,c,d]其中之一，组后用该结果取代[a,b,c,d]其中之一
                    #每次[a,b,c,d]顺序和环移量不同，四次一循环
                    order = orders[l]
                    const = const_list[j*16+k*4+l]
                    res = temp[order[0]]+item_list[i][group_order[j][4*k+l]]+const+fun_list[j](temp[order[1]],temp[order[2]],temp[order[3]])
                    res = res&0xffffffff
                    res = shift(res,offset[l])
                    res = (temp[order[1]]+res)&0xffffffff
                    temp[order[0]] = res
        for m in range(4):
            c_v[m] += temp[m]
            c_v[m] = c_v[m]&0xffffffff
#合并结果
def _merge():
    global c_v
    for i in range(4):
        c_v[i] = socket.ntohl(c_v[i])
    result = (c_v[0]<<96)+(c_v[1]<<64)+(c_v[2]<<32)+c_v[3]
    return result

raw_string = input("输入一个字符串：")
print("%032x" % encrypt(raw_string))