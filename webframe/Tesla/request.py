#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tesla.utils import syslog,status_code,tobtyes,tostring
from email.utils import formatdate
class Header:
    def __init__(self, encoding='utf-8'):
        self.content = {}
    def set(self,option,value):
        option = tostring(option)
        value = tostring(value)
        self.content[option] = value
    def get(self,option):
        try:
            result = self.content[option]
            return result
        except:
            syslog("Request Header不存在键:",option)
            return False
    def set_date(self):
        self.set('Date', tostring(formatdate(None, usegmt=True)))
    def __str__(self):
        result = None
        for item in self.content:
            result = result + item + ":" + self.content[item] + '\r\n'
        return result
class Request:
    def __init__(self,request,client,encoding = 'utf-8'):
        self.__client = client[0]
        self.__host = client[1][0]
        self.__port = client[1][1]
        if not isinstance(request,str):
            request = str(request,encoding=encoding)
        _slpit = request.split()
        _split_r_n = request.split('\r\n\r\n', 1)
        try:
            self.method = _slpit[0]
            self.path = _slpit[1]
            self.protocol_version = _slpit[2]
            self.headers = _split_r_n[0].split('\r\n')[1:]
            self.body = _split_r_n[1]
        except:
            self.method = False
            self.path = False
            self.protocol_version = False
            self.headers = False
            self.body = False
            syslog("Request解析错误")

        if self.headers != False:
            try:
                _headers = Header()
                for item in self.headers:
                    slpit = item.split(': ')
                    _headers.set(slpit[0],slpit[1])
                self.headers = _headers
            except:
                syslog("Request Header解析错误")
                self.headers = False

    def isregular(self):
        if self.method == False or self.protocol_version == False or self.path == False or self.headers == False or self.body == False:
            return False
        else:
            return True
    def COOKIES(self):
        pass
    def get_host(self):
        return self.__host
    def get_port(self):
        return self.__port
    def send(self,content):
        try:
            self.__client.send(content)
        except:
            pass
    def recv(self,number):
        self.__client.send(number)
    def close(self):
        self.__client.close()