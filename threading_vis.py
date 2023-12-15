#!/usr/bin/env python

# visualize.py
import argparse
import threading
import time
import datetime
import logging
from logging_config import setup_logging

# Setup logging using command-line arguments
def get_args():
    parser = argparse.ArgumentParser(description='Setup logging for the application.')
    parser.add_argument('--file', type=str, default='Banking.log', help='Log file name')
    parser.add_argument('--port', type=int, default=12345, help='Socket logging port')
    return parser.parse_args()

args = get_args()
logger = setup_logging(args.file, args.port)

def current_time():
    return time.time_ns()#datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

class MainThread:
    def __init__(self):
        self.thread = threading.current_thread()
        logger.info(f"{current_time()}, {self.thread.name}: {self.thread.ident}, 'Main thread initialized'")

    def watch_thread(self):
        while self.watchThread.is_alive():
            time.sleep(0.5)
            logger.info(f"{current_time()}, {self.thread.name}: {self.watchThread.ident}, 'Executing'")

        logger.info(f"{current_time()}, {self.thread.name}: {self.watchThread.ident}, 'Thread ended'")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"{current_time()}, {self.thread.name}: {self.thread.ident}, 'Main thread ended'")

def print(message):
    logger.info(f"PRINT: {message}")

class CreateThread:
    def __init__(self, name, target, args=()):
        self.thread = threading.Thread(name=name, target=target, args=args)

    def join(self):
        self.thread.join()
    
    def start(self):
        self.thread.start()
        logger.info(f"{current_time()}, {self.thread.name}: {self.thread.ident}, 'Thread started'")

class Lock:
    def __init__(self, name):
        self.lock = threading.Lock()
        self.name = name
        thread_name = threading.current_thread().name
        logger.info(f"{current_time()}, {thread_name}: {threading.current_thread().ident}, 'Lock {self.name} created'")

    def acquire(self):
        thread_name = threading.current_thread().name
        logger.info(f"{current_time()}, {thread_name}: {threading.current_thread().ident}, 'Lock {self.name} acquire request'")
        self.lock.acquire()
        logger.info(f"{current_time()}, {thread_name}: {threading.current_thread().ident}, 'Lock {self.name} acquired'")

    def release(self):
        thread_name = threading.current_thread().name
        logger.info(f"{current_time()}, {thread_name}: {threading.current_thread().ident}, 'Lock {self.name} release request'")
        self.lock.release()
        logger.info(f"{current_time()}, {thread_name}: {threading.current_thread().ident}, 'Lock {self.name} released'")
