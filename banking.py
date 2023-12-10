#!/usr/bin/env/ python

#----------------------------------------------------------------------
# banking.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

# Code adapted from
# https://www.educative.io/answers/what-are-locks-in-python
import ConcurrencyVis
import visualize
import time
import threading

# lock = visualize.lock("depositLock")
lock = visualize.lock("depositLock")
deposit = 100

def add_profit():
    global deposit
    for x in range(10):
        lock.acquire()
        time.sleep(0.5)
        deposit = deposit + 10
        lock.release()

def deduct_bill():
    global deposit
    for x in range(10):
        lock.acquire()
        deposit = deposit - 10
        lock.release()

add_thread = visualize.create_thread(name="add_profit", target=add_profit)
dep_thread = visualize.create_thread(name="deduct_bill", target=deduct_bill)

add_thread.join()
dep_thread.join()
print(deposit)

# print(lock.finalArray)
# lock.close()