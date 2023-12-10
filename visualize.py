#!/usr/bin/env/ python

#----------------------------------------------------------------------
# visualize.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

import os
import sys
import argparse
import threading
import datetime
import time


class create_thread():
    def __init__(self, name:str, target, args=()):
        # print("break 1")
        self.thread = threading.Thread(name=name, target=target, args=args)
        # print("break 2")
        self.thread.start()
        self.printArray = []
        if os.path.exists(self.thread.name):
            file = open(self.thread.name, "w")
        else:
            file = open(self.thread.name, "a")
        self.file = file
        # print("break 3")
        # print(threading.current_thread())
        # print(self.thread.is_alive())
        self.watchThread = threading.Thread(target=watch_thread, args=(self,))
        self.watchThread.start()

    def join(self):
        self.thread.join()

def watch_thread(thread: create_thread):
    now = datetime.datetime.now().strftime('%H:%M:%S')
    # file.write("Thread initialized at time " + now + "\n")
    # file.write("ID: " + str(thread.ident) + "\n")
    # file.write("Name of function: " + thread.name + "\n")
    # file.flush()
    thread.printArray.append("Thread initialized at time " + now + "\n")
    thread.printArray.append("ID: " + str(thread.thread.ident) + "\n")
    thread.printArray.append("Name of function: " + thread.thread.name + "\n")
    
    while(thread.thread.is_alive()):
        time.sleep(0.5)
        # file.write("Executing\n")
        # file.flush()
        thread.printArray.append("Executing\n")

    now = datetime.datetime.now().strftime('%H:%M:%S')
    # file.write("Thread ended at time " + now + "\n")
    # file.flush()
    # file.close
    thread.printArray.append("Thread ended at time " + now + "\n")
    thread.file.flush()
    for line in thread.printArray:
        thread.file.write(line)
    thread.file.flush()
    thread.file.close()

class lock():
    def __init__(self, name):
        self.lock = threading.Lock()
        # print("lock init")
        threadName = str(threading.currentThread().getName())
        # # self.lock = threading.Lock()
        self.name = name
        # self.finalArray = []
        file = open(threadName, "a")
        creationMsg = "Lock with name " + self.name + " created by "
        creationMsg += threadName + "\n"
        file.write(creationMsg)
        file.flush()
        file.close()

    def acquire(self):
        currentThread = str(threading.currentThread().getName())
        now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = "Lock with name " + self.name + " requested by "
        msg += currentThread + " at " + now + "\n"
        # self.finalArray.append((currentThread, msg))
        file = open(currentThread, "a")
        file.write(msg)
        file.flush()
        
        self.lock.acquire()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        msg = "Lock with name " + self.name + " acquired by "
        msg += currentThread + " at " + now + "\n"
        # self.finalArray.append((currentThread, msg))
        file.write(msg)
        file.flush()
        file.close()

    def release(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        currentThread = str(threading.currentThread().getName())
        msg = "Lock with name " + self.name + " attempted release by "
        msg += currentThread + " at " + now + "\n"
        # self.finalArray.append((currentThread, msg))
        file = open(currentThread, "a")
        file.write(msg)
        file.flush()
        
        self.lock.release()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        # # print("lock release")
        msg = "Lock with name " + self.name + " released by "
        msg += currentThread + " at " + now + "\n"
        # self.finalArray.append((currentThread, msg))
        file.write(msg)
        file.flush()
        file.close()
        # print(msg)
        # file = open(currentThread, "a")
        # file.write(msg)
        # file.close()

        # self.lock.release()

    # def close(self):
    #     for instance in self.finalArray:
    #         print(instance)
    #         file = open(instance[0], "a")
    #         file.write(instance[1])
    #         file.close
