#!/usr/bin/env python

# visualize.py
import argparse
import threading
import time
from logging_config import setup_logging

# Setup logging using command-line arguments
def get_args():
    parser = argparse.ArgumentParser(description='Setup logging for the application.')
    parser.add_argument('--file', type=str, default='Concurrency.log', help='Log file name')
    parser.add_argument('--port', type=int, default=12345, help='Socket logging port')
    return parser.parse_args()

args = get_args()
logger = setup_logging(args.file, args.port)

def current_time():
    return time.time_ns()

def custom_log(time, ident, textDescriptionWithName):
    logger.info(f"{time}, {ident}, {threading.current_thread().ident}, {textDescriptionWithName}")

class MainThread:
    def __init__(self):
        self.thread = threading.current_thread()
        custom_log(current_time(), threading.current_thread().ident, 'Main thread initialized')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        custom_log(current_time(), threading.current_thread().ident, 'Main thread ended')

class Thread:
    def __init__(self, name, target, args=()):
        self.thread = threading.Thread(name=name, target=target, args=args)
        # custom_log(current_time(), 'MainThread', threading.current_thread().ident, f"'{name} thread initialized'")

    def start(self):
        self.thread.start()
        custom_log(current_time(), self.thread.ident, f"'{self.thread.name}' thread started")

    def join(self):
        self.thread.join()
        custom_log(current_time(), self.thread.ident, f"'{self.thread.name}' thread joined")

    @property
    def ident(self):
        return self.thread.ident

    @property
    def name(self):
        return self.thread.name
 
class Lock:
    def __init__(self, name):
        self.lock = threading.Lock()
        self.name = name
        custom_log(current_time(), self.name, f"Lock '{self.name}' created")

    def acquire(self):
        # custom_log(current_time(), self.name, f"Lock '{self.name}' acquire request")
        self.lock.acquire()
        custom_log(current_time(), self.name, f"Lock '{self.name}' acquired")

    def release(self):
        custom_log(current_time(), self.name, f"Lock '{self.name}' released")
        self.lock.release()
        # custom_log(current_time(), self.name, f"Lock '{self.name}' released")

class Event:
    def __init__(self, name):
        self.event = threading.Event()
        self.name = name
        # custom_log(current_time(), self.name, f"Event {self.name} created")

    def set(self):
        self.event.set()
        custom_log(current_time(), self.name, f"Event {self.name} set")

    def clear(self):
        self.event.clear()
        custom_log(current_time(), self.name, f"Event {self.name} cleared")

    def wait(self, timeout=None):
        wait_result = self.event.wait(timeout)
        custom_log(current_time(), self.name, f"Event {self.name} wait, result: {wait_result}")
        return wait_result

    def is_set(self):
        is_set = self.event.is_set()
        # custom_log(current_time(), self.name, f"Event {self.name} is_set: {is_set}")
        return is_set

class Condition:
    def __init__(self, name):
        self.condition = threading.Condition()
        self.name = name
        # custom_log(current_time(), self.name, f"Condition {self.name} created")

    def __enter__(self):
        self.condition.acquire()
        custom_log(current_time(),  self.name, f"Condition {self.name} lock acquired by thread")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        custom_log(current_time(),  self.name, f"Condition {self.name} lock released by thread")
        self.condition.release()

    def acquire(self):
        self.condition.acquire()
        custom_log(current_time(), self.name, f"Condition {self.name} lock acquired")

    def release(self):
        custom_log(current_time(),  self.name, f"Condition {self.name} lock released")
        self.condition.release()

    def wait(self, timeout=None):
        custom_log(current_time(),  self.name, f"Condition {self.name} wait")
        self.condition.wait(timeout)

    def notify(self):
        self.condition.notify()
        custom_log(current_time(), self.name, f"Condition {self.name} notify")

    def notify_all(self):
        self.condition.notify_all()
        custom_log(current_time(),  self.name, f"Condition {self.name} notify_all")

class Barrier:
    def __init__(self, parties, name):
        self.barrier = threading.Barrier(parties)
        self.name = name
        # custom_log(current_time(),  self.name, f"Barrier {self.name} created with {parties} parties")

    def wait(self):
        # thread_name = threading.current_thread().name
        barrier_index = self.barrier.wait()
        custom_log(current_time(),  self.name,  f"Barrier {self.name} wait, index: {barrier_index}")
        return barrier_index

    def reset(self):
        self.barrier.reset()
        custom_log(current_time(),  self.name, f"Barrier {self.name} reset")

    def abort(self):
        self.barrier.abort()
        custom_log(current_time(), self.name,  f"Barrier {self.name} aborted")

    def parties(self):
        return self.barrier.parties

    def n_waiting(self):
        return self.barrier.n_waiting

    def broken(self):
        return self.barrier.broken
