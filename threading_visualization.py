#!/usr/bin/env python

# visualize.py
import argparse
import threading
import time
import uuid
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
    def __init__(self, silence=False):
        self.silence = silence
        self.thread = threading.current_thread()
        if not self.silence:
            custom_log(current_time(), threading.current_thread().ident, 'Main thread initialized')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.silence:
            custom_log(current_time(), threading.current_thread().ident, 'Main thread ended')

class Thread:
    def __init__(self, target, name='Thread_'+str(uuid.uuid4()), silence=False, args=()):
        self.silence = silence
        self.thread = threading.Thread(name=name, target=target, args=args)
        # custom_log(current_time(), 'MainThread', threading.current_thread().ident, f"'{name} thread initialized'")

    def start(self):
        self.thread.start()
        if not self.silence:
            custom_log(current_time(), self.thread.ident, f"'{self.thread.name}' thread started")

    def join(self):
        self.thread.join()
        if not self.silence:
            custom_log(current_time(), self.thread.ident, f"'{self.thread.name}' thread joined")

    @property
    def ident(self):
        return self.thread.ident

    @property
    def name(self):
        return self.thread.name
 
class Lock:
    def __init__(self, name='Lock_'+str(uuid.uuid4()),silence=False):
        self.lock = threading.Lock()
        self.name = name
        self.silence = silence
        if not self.silence:
            custom_log(current_time(), self.name, f"Lock '{self.name}' created")

    def acquire(self):
        # custom_log(current_time(), self.name, f"Lock '{self.name}' acquire request")
        self.lock.acquire()
        if not self.silence:
            custom_log(current_time(), self.name, f"Lock '{self.name}' acquired")

    def release(self):
        custom_log(current_time(), self.name, f"Lock '{self.name}' released")
        self.lock.release()
        # custom_log(current_time(), self.name, f"Lock '{self.name}' released")

class Event:
    def __init__(self, name='Event_'+str(uuid.uuid4()),silence=False):
        self.event = threading.Event()
        self.name = name
        self.silence = silence
        # custom_log(current_time(), self.name, f"Event {self.name} created")

    def set(self):
        self.event.set()
        if not self.silence:
            custom_log(current_time(), self.name, f"Event {self.name} set")

    def clear(self):
        self.event.clear()
        if not self.silence:
            custom_log(current_time(), self.name, f"Event {self.name} cleared")

    def wait(self, timeout=None):
        wait_result = self.event.wait(timeout)
        if not self.silence:
            custom_log(current_time(), self.name, f"Event {self.name} wait, result: {wait_result}")
        return wait_result

    def is_set(self):
        is_set = self.event.is_set()
        # custom_log(current_time(), self.name, f"Event {self.name} is_set: {is_set}")
        return is_set

class Condition:
    def __init__(self, name='Condition_'+str(uuid.uuid4()),silence=False):
        self.condition = threading.Condition()
        self.name = name
        self.silence = silence
        # custom_log(current_time(), self.name, f"Condition {self.name} created")

    def __enter__(self):
        self.condition.acquire()
        if not self.silence:
            custom_log(current_time(),  self.name, f"Condition {self.name} lock acquired by thread")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.silence:
            custom_log(current_time(),  self.name, f"Condition {self.name} lock released by thread")
        self.condition.release()

    def acquire(self):
        self.condition.acquire()
        if not self.silence:
            custom_log(current_time(), self.name, f"Condition {self.name} lock acquired")

    def release(self):
        if not self.silence:
            custom_log(current_time(),  self.name, f"Condition {self.name} lock released")
        self.condition.release()

    def wait(self, timeout=None):
        if not self.silence:
            custom_log(current_time(),  self.name, f"Condition {self.name} wait")
        self.condition.wait(timeout)

    def notify(self):
        self.condition.notify()
        if not self.silence:
            custom_log(current_time(), self.name, f"Condition {self.name} notify")

    def notify_all(self):
        self.condition.notify_all()
        if not self.silence:
            custom_log(current_time(),  self.name, f"Condition {self.name} notify_all")

class Barrier:
    def __init__(self, parties, name='Barrier_'+str(uuid.uuid4()),silence=False):
        self.barrier = threading.Barrier(parties)
        self.name = name
        self.silence = silence
        # custom_log(current_time(),  self.name, f"Barrier {self.name} created with {parties} parties")

    def wait(self):
        # thread_name = threading.current_thread().name
        barrier_index = self.barrier.wait()
        if not self.silence:
            custom_log(current_time(),  self.name,  f"Barrier {self.name} wait, index: {barrier_index}")
        return barrier_index

    def reset(self):
        self.barrier.reset()
        if not self.silence:
            custom_log(current_time(),  self.name, f"Barrier {self.name} reset")

    def abort(self):
        self.barrier.abort()
        if not self.silence:
            custom_log(current_time(), self.name,  f"Barrier {self.name} aborted")

    def parties(self):
        return self.barrier.parties

    def n_waiting(self):
        return self.barrier.n_waiting

    def broken(self):
        return self.barrier.broken
