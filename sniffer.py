#this is a simple sniffer
import socket
import os
import struct
from ctypes import *
import chardet
import re

#ip header
#----------------------32bit-----------------------------------------------------------------------------------------------------
#		8		|		8		|		8		|		8		|
#--------------------------------------------------------------------------------------------------------------------------------
#	版本4	|	包头长4|			服务类型8	|				总长16				|
#--------------------------------------------------------------------------------------------------------------------------------
#				标识16				|	标志3|			偏移13			|
#--------------------------------------------------------------------------------------------------------------------------------
#		TTL8		|		协议8		|			checksum16			|
#--------------------------------------------------------------------------------------------------------------------------------
#						source_addr								|
#--------------------------------------------------------------------------------------------------------------------------------
#						des_addr								|
#--------------------------------------------------------------------------------------------------------------------------------
#						Option	and padding							|
#--------------------------------------------------------------------------------------------------------------------------------

# host to listen on
host = "169.254.215.140"

#inherent Structure or Union
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
    #create
    def __new__(self, socket_buffer=None):
		#返回一个ctypes实例,此处是IP类的实例(继承)
        return self.from_buffer_copy(socket_buffer)
    #initialize
    def __init__(self, socket_buffer=None):
        # map protocol constants to their names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        # human readable IP addresses,<L unsign long little-endian
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))
        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
        #2F00 -> 002F,总长
        self.length = socket.ntohs(self.len)
        #ip头长
        self.header_length = self.ihl*4;
        #identifier标志
        self.label = socket.ntohs(self.id)
        #offset
        self.off_set = socket.ntohs(self.offset)&0b1111111111111
        #flag标识 3bit 第二位表示是否分片，第三位表示若分片后面还有没有分片
        self.flag = socket.ntohs(self.offset)>>13

# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 60001))
# we want the IP headers included in the capture.
# On the other hand,a TCP/IP service provider that supports SOCK_RAW should also support IP_HDRINCL.
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#recv all
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
try:
    while True:
        # read in a single packet,[data,src]
        raw_buffer = sniffer.recvfrom(65535)
        #数据
        raw_buffer = raw_buffer[0]
        #IP header
        ip_split = IP(raw_buffer[0:20])
        print("Protocol: %s %s -> %s" % (ip_split.protocol, ip_split.src_address, ip_split.dst_address))
        print("包头:%d" % ip_split.header_length)
        print("数据长度:%d字节" % (ip_split.length-40))
        print("偏移:%d字节" % (ip_split.off_set))
        print("标识:%s" % ip_split.label)
        print("标志位:%s" % bin(ip_split.flag))
        
		#extra data
        if(ip_split.length != 40):
            enc = chardet.detect(raw_buffer[40:])['encoding']
            if(enc):
                try:
                    print("数据:%s" % raw_buffer[40:].decode(enc))
                except:
                    print("Decode Error!!!")
            else:
                print("Unknow Encoding!")
        else:
            print("No Data!!!")
        print('-------------------------------')
except KeyboardInterrupt:
	if os.name == "nt":
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
