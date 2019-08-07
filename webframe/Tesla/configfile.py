#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser
from Tesla.utils import syslog

class ConfigFile:
    def __init__(self,config_file_name,encoding = 'utf8'):
        self.__file_name = config_file_name
        self.__config = configparser.ConfigParser()
        self.__config.read(config_file_name, encoding=encoding)
        try:
            file = open(self.__file_name)
            file.close()
        except:
            syslog('打开配置文件时发生错误',config_file_name)
        if self.__config.sections() == []:
            syslog("配置文件内容丢失:",config_file_name)
    def get_section(self):
        return self.__config.sections()
    def get_option(self,section):
        return self.__config.options(section)
    def get_items(self,section):
        return self.__config.items(section)
    def has_section(self,section):
        return self.__config.has_section(section)
    def has_option(self,section,option):
        return self.__config.has_option(section,option)
    def get_option_value(self,section,option):
        try:
            container = self.__config.get(section,option)
        except:
            syslog("获取配置文件",self.__file_name,"键值发生错误:",section,option)
            return False
        return container
    def get_option_value_dict(self,section):
        config_dict = {}
        common_option = self.get_option(section)
        for item in common_option:
            config_dict[item] = self.get_option_value(section,item)
        return config_dict
    def set_option_value(self,section,option,value):
        try:
            self.__config.set(section,option,value)
            file = open(self.__file_name)
            self.__config.write(file)
            file.close()
            return True
        except:
            syslog("设置配置文件",self.__file_name,"键值发生错误:", section, option)
            return False

class CommonConfig(ConfigFile):
    def __init__(self,config_file_name,encoding = 'utf8'):
        ConfigFile.__init__(self,config_file_name,encoding =encoding)
        self.__common_section = 'Common'
        self.common_config_dict = self.get_option_value_dict(self.__common_section)
    def dict(self):
        return self.common_config_dict
    def ip(self):
        return self.dict()['host_ip']
    def port(self):
        return int(self.dict()['host_port'])
    def encode(self):
        return self.dict()['encode']
    def max_listen(self):
        return int(self.dict()['max_listen'])
    def max_connect(self):
        return int(self.dict()['max_connect'])