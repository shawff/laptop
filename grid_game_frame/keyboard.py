from pynput.keyboard import Key,Listener
import threading
import queue
import time

class KeyboardListenThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID,message_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.message_queue = message_queue
        self.stopflag = False

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        with Listener(on_press=self.on_press,on_release=self.on_release) as self.listener:
            self.listener.join()
    def on_press(self,key):
        pass
    def on_release(self,key):
        if self.stopflag == True:
            return False
        # 监听
        self.message_queue.put(key)
    def ListenClose(self):
        self.stopflag = True

# 创建并开启新线程
messagequeue = queue.Queue()
thread = KeyboardListenThread(1, messagequeue)
thread.start()





