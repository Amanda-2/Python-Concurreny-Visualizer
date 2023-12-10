#!/usr/bin/env/ python

#----------------------------------------------------------------------
# concurrencyVis.py
# Authors: Amanda Sparks and Luke Shannon
#----------------------------------------------------------------------

import threading
import ConcurrencyVis
import time
import visualize

def addition_thread():
    for x in range(0, 80):
        time.sleep(0.5)
        #print(x + (x+1))
        print("adding : " + str(x))
    
def subtraction_thread():
    for x in range(0, 80):
        time.sleep(0.5)
        # print(x - (80-x))
        print("subtracting : " + str(x))

def multiplication_thread():
    for x in range(0, 80):
        time.sleep(0.5)
        # print(x*(x+1))
        print("multiplication : " + str(x))

def division_thread():
    for x in range(0, 80):
        time.sleep(0.5)
        # print(x//(x+1))
        print("division : " + str(x))

def main():

    # Do not redeclare .start(). create_thread already starts thread
    visualize.create_thread("addition_thread", addition_thread)
    visualize.create_thread("subtraction_thread", subtraction_thread)
    visualize.create_thread("multiplication_thread", multiplication_thread)
    visualize.create_thread("division_thread", division_thread)

if __name__ == '__main__':
    main()