import os
import threading
import time
import csv
import psutil
from queue import Queue
from statistics import mean
from threading import Thread


def get_current_memory_usage():
    return round(psutil.Process(os.getpid()).memory_info().rss * 100 / psutil.virtual_memory().total, 3)


def get_current_cpu_usage():
    process = psutil.Process(os.getpid())
    usage = process.cpu_percent(interval=1)
    return round(usage, 3)


class Timer():
    def __init__(self, name):
        print()
        print("Starting '{}' benchmark...".format(name))
        self.name = name
        self.memory_samples_queue = Queue()
        self.cpu_samples_queue: Queue = Queue()
        self.stop_event: threading.Event = threading.Event()
        self.record_thread: Thread = Thread(target=self.record_metric,
                                            args=[self.stop_event, self.cpu_samples_queue, self.memory_samples_queue],
                                            daemon=True)
        self.record_thread.start()
        self.start = time.time()
        self.cpu_samples_queue.put(get_current_cpu_usage())
        self.memory_samples_queue.put(get_current_memory_usage())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        runtime = self.float_to_string(time.time() - self.start)
        self.stop_event.set()
        self.record_thread.join()
        print(self.get_values_from_queue(self.cpu_samples_queue))
        cpu_usage = self.float_to_string(mean(self.get_values_from_queue(self.cpu_samples_queue)), True)
        memory_usage = self.float_to_string(mean(self.get_values_from_queue(self.memory_samples_queue)), True)
        print('Benchmark took {} seconds, used {} CPU and {} RAM'.format(runtime, cpu_usage, memory_usage))
        self.store_result(runtime, cpu_usage, memory_usage)
        time.sleep(3)  # Need to wait for waiting resources to be freed up

    def float_to_string(self, value: float, add_percent=False):
        result = str(round(value, 3)).replace('.', ',')
        if add_percent:
            return result + "%"
        return result

    def get_values_from_queue(self, queue: Queue):
        values = []
        while not queue.empty():
            values.append(queue.get())
        return values

    def store_result(self, runtime, cpu_usage, memory_usage):
        with open("results.csv", "a") as results:
            writer = csv.writer(results, delimiter=";")
            writer.writerow([self.name, runtime, cpu_usage, memory_usage])

    def record_metric(self, stop_event: threading.Event, cpu_queue: Queue, memory_queue: Queue):
        while not stop_event.wait(0.200):
            cpu_queue.put(get_current_cpu_usage())
            memory_queue.put(get_current_memory_usage())
