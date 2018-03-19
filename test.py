import socket
import os
import struct
from ctypes import *
import chardet
import re

# host to listen on
host = "169.254.158.90"

#必须继承Structure或者Union
class IP(Structure):
	_fields_ = [
			("ihl", c_ubyte, 4),
			("version", c_ubyte, 4),
			("tos", c_ubyte),
			("len", c_ushort),
			("id", c_ushort),
			("offset", c_ushort),
			("ttl", c_ubyte),
			("protocol_num", c_ubyte),
			("sum", c_ushort),
			("src", c_ulong),
			("dst", c_ulong)
		]
	def __new__(self, socket_buffer=None):
		print("new")
		print(type(self))
		print(type(self.from_buffer_copy(socket_buffer)))
		return self.from_buffer_copy(socket_buffer)
	#构造函数
	def __init__(self, socket_buffer=None):
		# map protocol constants to their names
		print('init')
		print(type(self))


s = b'12345678901234567890'
IP(s)