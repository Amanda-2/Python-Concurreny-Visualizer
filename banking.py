import threading_vis as visualize
import time

# Initialize global variables
deposit = 100
deposit_lock = visualize.Lock("depositLock")

def add_profit():
    global deposit, deposit_lock
    for x in range(10):
        deposit_lock.acquire()
        time.sleep(0.1)
        deposit = deposit + 10
        deposit_lock.release()

def deduct_bill():
    global deposit, deposit_lock
    for x in range(10):
        deposit_lock.acquire()
        time.sleep(0.1)
        deposit = deposit - 10
        deposit_lock.release()

def main():
    with visualize.MainThread():
        visualize.print("Starting banking.py")

        global deposit, deposit_lock

        add_thread = visualize.CreateThread(name="add_profit", target=add_profit)
        dep_thread = visualize.CreateThread(name="deduct_bill", target=deduct_bill)

        add_thread.start()
        dep_thread.start()

        visualize.print("Middle of banking.py, threads started")

        add_thread.join()
        dep_thread.join()

        print(deposit)
        visualize.print(f"End of banking.py, final deposit: {deposit}")

if __name__ == "__main__":
    main()
