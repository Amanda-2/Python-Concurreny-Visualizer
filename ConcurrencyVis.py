#!/usr/bin/env/ python

#----------------------------------------------------------------------
# concurrencyVis.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

import os
import sys
import argparse
import threading
import datetime

# DEPRECATED, DO  NOT USE
class VisualizeThread (threading.Thread):
    def __init__(self, name, target, args=(), kwargs={}):
        print("VisualizeThread init")
        # self.thread = threading.Thread.__init__(self, target=target, name=name, args=args, kwargs=kwargs)
        print(target)
        self.thread = threading.Thread.__init__(self, target=target, name=name, args=args, kwargs=kwargs)
        self.ID = threading.get_ident()
        self.name = name
        self.filename = str(self.ID)
        self.file = open(self.name, "w")

        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.file.write("Thread initialized at time " + now + "\n")
        self.file.write("ID: " + self.filename + "\n")
        self.file.write("Name of function: " + self.name + "\n")
        
        threading.settrace(track(self))

def lock():
    print("lock created by " + str(threading.currentThread().getName))
    return threading.Lock()


# def track(thread: threading.Thread):
def track(frame, event, arg):
    print("entered tracking")
    if thread == threading.main_thread():
        file = open("main", "w")
        file.write = "Main thread executing"
    else:
#     while thread.is_alive():
#         print(str(threading.currentThread().getName))
#     #     thread.file.write("Executing: " + thread.name + "\n")
        thread.file.write("State: " + str(thread.is_alive()))
        thread.file.write("Executing: " + thread.name + "\n")
    print()

def settrace(function):
    threading.settrace(function)

def main_thread():
    return threading.main_thread()
        
        

# def main():
#     dummy()
#     print("Entered ConcurrencyVis main")

# if __name__ == main:
#     main()
