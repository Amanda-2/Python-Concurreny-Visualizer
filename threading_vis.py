#!/usr/bin/env/ python

#----------------------------------------------------------------------
# visualize.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

import threading
import datetime
import time

class main_thread():
    def __init__(self):
        self.thread = threading.current_thread()
        # self.file = open("MainThread", "a")
        # open 
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.file.write(now + " Main thread initialized\n")
        self.printArray=[]
        self.watchThread = threading.Thread(target=watch_thread, args=(self,))
        self.watchThread.start()

class create_thread():
    def __init__(self, name:str, target, args=()):
        self.thread = threading.Thread(name=name, target=target, args=args)
        self.thread.start()
        self.printArray = []
        self.file = open(self.thread.name, "a")
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.file.write(now + " 0 Thread initialized\n")
        self.file.write(now + " 1 ID: " + str(self.thread.ident) + "\n")
        self.file.write(now + " 2 Name of function: " + self.thread.name + "\n")
        self.file.flush()

        self.watchThread = threading.Thread(target=watch_thread, args=(self,))
        self.watchThread.start()

    def join(self):
        self.thread.join()

def watch_thread(thread: create_thread):

    while(thread.thread.is_alive()):
        time.sleep(0.5)

        now = datetime.datetime.now().strftime('%H:%M:%S')
        thread.printArray.append(now + " Executing\n")

    now = datetime.datetime.now().strftime('%H:%M:%S')
    thread.printArray.append(now + " Thread ended at time " + now + "\n")
    thread.file.flush()
    for line in thread.printArray:
        thread.file.write(line)
    thread.file.flush()
    thread.file.close()

class lock():
    def __init__(self, name):
        self.lock = threading.Lock()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        threadName = str(threading.currentThread().getName())
        self.name = name
        file = open(threadName, "a")
        creationMsg = now + " Lock with name " + self.name + " created by "
        creationMsg += threadName + "\n"
        file.write(creationMsg)
        file.flush()
        file.close()

    def acquire(self):
        currentThread = str(threading.currentThread().getName())
        now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = now + " 3 Lock with name " + self.name + " requested by "
        msg += currentThread + "\n"
        file = open(currentThread, "a")
        file.write(msg)
        file.flush()
        
        self.lock.acquire()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = now + " 4 Lock with name " + self.name + " acquired by "
        msg += currentThread + "\n"
        file.write(msg)
        file.flush()
        file.close()

    def release(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        currentThread = str(threading.currentThread().getName())
        msg = now + " 5 Lock with name " + self.name + " attempted release by "
        msg += currentThread + "\n"
        file = open(currentThread, "a")
        file.write(msg)
        file.flush()
        
        self.lock.release()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = now + " 6 Lock with name " + self.name + " released by "
        msg += currentThread + "\n"
        file.write(msg)
        file.flush()
        file.close()

def filesort(filename: str):
    file = open(filename, "r")
    data = file.readlines()
    file.close()
    file = open(filename, "w")
    data.sort()
    for line in data:
        file.write(line)
        file.flush()
    file.close()
