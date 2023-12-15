import time
import argparse
from threading_visualization import Thread, MainThread, Lock

def worker_task(lock, worker_name, sleep_time):
    lock.acquire()
    print(f"{time.time_ns()}, {worker_name}: Working.")
    time.sleep(sleep_time)
    lock.release()
    print(f"{time.time_ns()}, {worker_name}: Finished working.")

def main(n, sleep_time):
    lock = Lock("shared_lock")

    with MainThread():
        workers = []
        for i in range(n):
            worker_name = f"Worker{i + 1}"
            worker = Thread(worker_name, target=worker_task, args=(lock, worker_name, sleep_time))
            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run worker threads with shared lock.')
    parser.add_argument('--num_workers', type=int, default=50, help='Number of worker threads')
    parser.add_argument('--sleep_time', type=int, default=0.1, help='Sleep time for each worker (in seconds)')
    args = parser.parse_args()

    main(args.num_workers, args.sleep_time)