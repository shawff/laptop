#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tesla.request import Header,Request
from Config.settings import *
from Tesla.utils import tostring,tobtyes,status_code
import gzip
#import StringIO
import threading

class HttpResponse:
    def __init__(self,requset,content,content_type=None, statue=None):
        self.__requset = requset
        self.__frist_line = self.frist_line(statue)
        if isinstance(content,int):
            content = str(content)
        self.__body = tobtyes(content)
        self.set_header(content_type)
        self.__requset.send(self.content())

    def frist_line(self,statue):
        """第一行"""
        self.__protocol = self.__requset.protocol_version
        if statue != None:
            self.__statue = str(statue)
        else:
            self.__statue = 200
        self.__status_name = status_code(self.__statue)

    def set_header(self,content_type):
        """设置头部"""
        self.__headers = Header()
        self.__headers.set_date()
        content_encoding = self.__requset.headers.get('Accept-Encoding')
        if content_encoding != False:
            if content_encoding.find('gzip')>=0:
                self.gzip_body()
            else:
                self.set_body()
        else:
            self.set_body()
        if content_type != None:
            self.__headers.set('Content-Type', content_type)
        else:
            self.__headers.set('Content-Type','text/html;charset=utf-8')

        connection = self.__requset.headers.get('Connection')
        if connection != False:
            self.__headers.set('Connection', connection)
        self.__headers.set('Cache - Control', 'max - age = 0')


    def content(self):
        blank = ' '
        split = '\r\n'
        self.__response = tostring(self.__protocol) + blank + tostring(self.__statue) + blank + tostring(self.__status_name) + split
        if self.__headers != {}:
            for item in self.__headers.content:
                self.__response = self.__response + item + ':' + self.__headers.content[item] + split
        self.__response = self.__response + split
        if self.__body != None:
            self.__response = tobtyes(self.__response)  + self.__body
        return self.__response

    def set_body(self):
        self.__headers.set('Content-Encoding', 'deflate')
        length = len(self.__body)
        self.__headers.set('Content-Length', str(length))


    def gzip_body(self):
        self.__headers.set('Content-Encoding', 'gzip')
        self.__body = gzip.compress(self.__body)
        length = len(self.__body)
        self.__headers.set('Content-Length', str(length))

def render(requset, template_name, statue=None):
    class simple_thread(threading.Thread):
        def __init__(self, function,requset, template_name, statue=None):
            threading.Thread.__init__(self)
            self.function = function

        def run(self):
            self.function(requset, template_name, statue=None)
    def function(requset, template_name, statue=None):
        template_name = BASE_DIR+template_name
        #print(template_name)
        content = open(template_name,encoding='utf-8')
        content = content.read()
        return HttpResponse(requset,content,statue)
    thread = simple_thread(function,requset, template_name, statue=None)
    thread.start()