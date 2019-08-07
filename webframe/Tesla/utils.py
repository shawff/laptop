#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
rep_status = {'100':'Continue',
         '101':'Switching Protocols',
         '200':'OK',
          '201': 'Created',
          '202': 'Accepted',
          '203': 'Non - Authoritative Information',
          '204': 'No Content',
          '205': 'Reset Content',
          '206': 'Partial Content',
          '300': 'Multiple Choices',
          '301': 'Moved Permanently',
          '302': 'Found',
          '303': 'See Other',
          '304': 'Not Modified',
          '305': 'Use Proxy',
          '306': 'Unused',
          '307': 'Temporary Redirect',
          '400': 'Bad Request',
          '401': 'Unauthorized',
          '402': 'Payment Required',
          '403': 'Forbidden',
          '404': 'Not Found',
          '405': 'Method Not Allowed',
          '406': 'Not Acceptable',
          '407': 'Proxy Authentication Required',
          '408': 'Request Time - out',
          '409': 'Conflict',
          '410': 'Gone',
          '411': 'Length Required',
          '412': 'Precondition Failed',
          '413': 'Request Entity Too Large',
          '414': 'Request-URI Too Large',
          '415': 'Unsupported Media Type',
          '416': 'Requested range not satisfiable',
          '417': 'Expectation Failed',
          '500': 'Internal Server Error',
          '501': 'Not Implemented',
          '502': 'Bad Gateway',
          '503': 'Service Unavailable',
          '504': 'Gateway Time-out	',
          '505': 'HTTP Version not supported'
          }

def syslog(*content):
    try:
        for index in content:
            if isinstance(index,str) == False:
                index = str(index)
            sys.stderr.write(index  )
    except:
        pass

def status_code(status):
    try:
        status = tostring(status)
        result = rep_status[status]
        return result
    except:
        syslog("状态码不存在:",status)
        return False

def tostring(content, encoding='utf-8'):
    if isinstance(content,bytes) == True:
        return str(content, encoding=encoding)
    else:
        return str(content)
def tobtyes(content,encoding = 'utf-8'):
    if isinstance(content, str) == True:
        return bytes(content, encoding=encoding)
    else:
        return bytes(content)
