import time
import csv
from statistics import mean
from threading import Thread

import psutil


class Timer():
    def __init__(self, name):
        self.start = time.time()
        self.record_data = {
            "is_on": True,
            "cpu_records": [],
            "memory_records": [],
        }
        self.name = name
        self.record_thread = Thread(target=self.record_metric, args=[self.record_data], daemon=True).start()
        print()
        print("Starting '{}' benchmark...".format(self.name))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.record_data["is_on"] = False
        runtime = str(round(time.time() - self.start, 3)).replace(".", ",")
        cpu_usage = str(round(mean(self.record_data["cpu_records"]), 3)).replace('.', ',') + "%"
        memory_usage = str(round(mean(self.record_data["memory_records"]), 3)).replace('.', ',') + "%"
        print('Benchmark took {} seconds, used {} CPU and {} RAM'.format(runtime, cpu_usage, memory_usage))
        self.store_result(runtime, cpu_usage, memory_usage)
        time.sleep(3)  # Need to wait for waiting resources to be freed up

    def store_result(self, runtime, cpu_usage, memory_usage):
        with open("results.csv", "a") as results:
            writer = csv.writer(results, delimiter=";")
            writer.writerow([self.name, runtime, cpu_usage, memory_usage])

    def record_metric(self, record_data):
        while record_data["is_on"]:
            record_data["cpu_records"].append(psutil.cpu_percent())
            record_data["memory_records"].append(psutil.virtual_memory().percent)
            time.sleep(0.005)
