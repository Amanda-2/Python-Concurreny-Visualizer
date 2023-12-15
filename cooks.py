import threading_visualization as threading
import time

def chef_work(lock, event, condition, barrier, name):
    # Simulate preparing ingredients
    time.sleep(0.5)
    print(f"{name}: Ingredients prepared.")

    # Waiting for the oven to be free
    lock.acquire()
    print(f"{name}: Using the oven.")
    time.sleep(1)  # Simulate time taken to use the oven
    lock.release()
    print(f"{name}: Done with the oven.")

    # Signal that part of the meal is ready
    with condition:
        print(f"{name}: Dish is ready to plate.")
        condition.notify()

    # Wait for all dishes to be ready
    event.wait()
    print(f"{name}: All dishes ready.")

    # Synchronize plating
    barrier.wait()
    print(f"{name}: Plating the meal.")

def main():
    args = threading.get_args()
    # logger = threading.setup_logging(args.file, args.port)

    # Initialize concurrency primitives
    lock = threading.Lock("oven_lock")
    event = threading.Event("meal_ready_event")
    condition = threading.Condition("dish_ready_condition")
    barrier = threading.Barrier(2, "plating_barrier")

    # Start chefs (threads)
    with threading.MainThread():
        chef1 = threading.Thread("Chef1", target=chef_work, args=(lock, event, condition, barrier, "Chef1"))
        chef2 = threading.Thread("Chef2", target=chef_work, args=(lock, event, condition, barrier, "Chef2"))

        chef1.start()
        chef2.start()

        # Main thread simulates coordinating the kitchen
        with condition:
            condition.wait()  # Wait for a chef to signal that a dish is ready

        print("Main thread: Final dish being prepared.")
        time.sleep(1)  # Simulate final preparation time
        event.set()  # Signal that all dishes are ready

        chef1.join()
        chef2.join()

if __name__ == "__main__":
    main()
