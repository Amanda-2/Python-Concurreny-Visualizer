# CODE TAKEN DIRECTLY FROM https://www.pythontutorial.net/python-concurrency/python-threading-lock/
# to demonstrate the ease of translating from threading to the threading_visualization module

# from threading import Thread, Lock
from threading_visualization import Thread, Lock, MainThread
from time import sleep


with MainThread(file="Lock.log"): # added line
    counter = 0


    def increase(by, lock):
        global counter

        lock.acquire()

        local_counter = counter
        local_counter += by

        sleep(0.1)

        counter = local_counter
        print(f'counter={counter}')

        lock.release()


    lock = Lock()

    # create threads
    t1 = Thread(target=increase, args=(10, lock))
    t2 = Thread(target=increase, args=(20, lock))

    # start the threads
    t1.start()
    t2.start()


    # wait for the threads to complete
    t1.join()
    t2.join()


    print(f'The final counter is {counter}')