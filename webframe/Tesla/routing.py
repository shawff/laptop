#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from Config import urls
from Config.settings import *
from Tesla.response import HttpResponse,render
import threading
class Routing:
    def __init__(self,request):
        self.__request = request
        self.__list = urls.urlpatterns
        class __simple_thread(threading.Thread):
            def __init__(self, function, requset):
                threading.Thread.__init__(self)
                self.function = function
                self.requset = requset
            def run(self):
                self.function(self.requset)

        in_list = False
        for item in self.__list:
            path = item[0]
            func = item[1]
            if   path == self.__request.path:
                in_list = True
                thread = __simple_thread(func,request)
                thread.start()
                break

        if  in_list == False:
            path =self.__request.path.replace('/','\\')
            result = os.path.exists(BASE_DIR+path)
            #print(path,result)
            if result == True:
                print(self.__request.path,"成功打开")
                render(self.__request,path)
            else:
                HttpResponse(self.__request,'404',None,404)