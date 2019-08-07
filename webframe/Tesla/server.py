#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

import queue
from Tesla.configfile import CommonConfig
from Tesla.request import Request
import socket  # 导入 socket 模块
import threading
from Tesla.utils import syslog,status_code,tobtyes,tostring
from Tesla.routing import Routing
import time


class Web:
    def __init__(self,config_file_name):
        self.comconfig = CommonConfig(config_file_name)
        self.__sock = socket.socket()
        self.__ip = self.comconfig.ip()
        self.__port = self.comconfig.port()
        self.__max_listen = self.comconfig.max_listen()
        self.__max_connect = self.comconfig.max_connect()
        self.__connect_number = 0
        self.__sock.setblocking(0)

        self._client_list = queue.Queue()

        class simple_thread(threading.Thread):
            def __init__(self, function):
                threading.Thread.__init__(self)
                self.function = function

            def run(self):
                self.function()

        self._bind()
        self._listen(self.__max_listen)
        accept_thread = simple_thread(self._accept)
        accept_thread.start()



    def _bind(self):
        self.__sock.bind((self.__ip, self.__port))  # 绑定端口

    def _listen(self,backlog):
        __backlog = int(backlog)
        self.__sock.listen(__backlog)
    def _accept(self):
        while True:
             try:
                 client,addr = self.__sock.accept()
                 print("连接：",addr[0],addr[1])
                 thread = WebDriver((client, addr),self.comconfig)
                 thread.start()
             except:
                pass
    """
    双线程
    accept_thread = simple_thread(self._accept)
    accept_thread.start()
    client_thread = simple_thread(self._client_thread)
    client_thread.start()
    def _accept(self):
        while True:
            #if self.__connect_number<self.__max_connect:
                try:
                    client,addr = self.__sock.accept()
                    print("连接：",addr[0],addr[1])
                    self._client_list.put((client,addr))
                    self.__connect_number = self.__connect_number + 1
                except:
                    pass
    def _client_thread(self):
        while True:
            if self._client_list.empty() == False:
                client= self._client_list.get()
                thread = WebDriver(client,self.comconfig)
                thread.start()
                self.__connect_number = self.__connect_number - 1
            else:
                time.sleep(0.1)
    """

    def _clost_connect(self,host):
        host.close()
    def __del__(self):
        del(self._client_list)
        self.__sock.close()


class WebDriver(threading.Thread):
    def __init__(self,client,config):
        threading.Thread.__init__(self)
        self._client = client[0]
        self._addr = client[1]
        self._config = config
        self._encode = self._config.encode()

    def run(self):
        counter = 0
        while True:
            req_btyes = None
            if counter > 100000:
                #print('关闭连接:',self._addr)
                self._client.close()
                break
            try:
                req_btyes =  self._client.recv(2048)
                req_str = tostring(req_btyes)
                req = Request(req_str, (self._client, self._addr))
                # print(req_str)
                # 非正常请求
                if req.isregular() == False:
                    msg_btyes = tobtyes('HTTP/1.1 400 Bad Request\r\n')
                    self._client.send(msg_btyes)
                    return
                Routing(req)
            except:
                counter = counter +1




if __name__ == '__main__':
    web = Web('Config.ini')
