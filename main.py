import json

import psutil

from timer import Timer
from benchmarks import json_loads_test, aggregation_from_dict_test, regexp_test
from utils import formatByteSize


def get_test_data_as_string():
    with open("test.json", "r") as file:
        return file.read()


def get_test_data_as_json():
    with open("test.json", "r") as file:
        return json.loads(file.read())


def prepare_results_csv():
    with open("results.csv", "w") as results:
        results.write("Benchmark name;runtime;cpu usage;memory usage\n")


def main():
    print("************************")
    print("*** Python benchmark ***")
    print("************************")
    print()
    print("Available CPU cores: {} Current CPU usage: {}%".format(psutil.cpu_count(), psutil.cpu_percent()))
    print("Available Memory: {} Current Memory usage: {}%".format(formatByteSize(psutil.virtual_memory().total),
                                                                  psutil.virtual_memory().percent))
    test_data_as_json = get_test_data_as_json()
    test_data_as_string = get_test_data_as_string()
    prepare_results_csv()

    with Timer("Testing regexp for digits"):
        regexp_test(test_data_as_string)

    with Timer("Testing importing big json file into python"):
        json_loads_test()

    with Timer("Testing aggregating column from dict and counting median"):
        aggregation_from_dict_test(test_data_as_json)

    print("Done!")


if __name__ == '__main__':
    main()
