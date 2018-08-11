import sys

from timer import *
from benchmarks import *
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


def print_welcome_message():
    print("************************")
    print("*** Python benchmark ***")
    print("************************")
    print()
    print("Available CPU cores: {} Current CPU usage: {}%".format(psutil.cpu_count(), psutil.cpu_percent()))
    print("Available Memory: {} Current Memory usage: {}%".format(formatByteSize(psutil.virtual_memory().total),
                                                                  get_current_memory_usage()))


def main():
    sys.setrecursionlimit(2147483647)
    test_data_as_json = get_test_data_as_json()
    test_data_as_string = get_test_data_as_string()
    prepare_results_csv()
    unsorted_list_of_numbers = re.findall("[+-]?\d+(?:\.\d+)?", test_data_as_string)
    unsorted_list_of_numbers = unsorted_list_of_numbers[:int(len(unsorted_list_of_numbers) / 11)]

    print_welcome_message()

    with Timer("B tree"):
        binarytree_test()

    with Timer("Quick sort"):
        quick_sort_test(unsorted_list_of_numbers)

    with Timer("Merge sort"):
        merge_sort(unsorted_list_of_numbers)

    with Timer("Regexp for digits"):
        regexp_test(test_data_as_string)

    with Timer("Importing big json file into python"):
        json_loads_test()

    with Timer("Aggregating column from dict and counting median"):
        aggregation_from_dict_test(test_data_as_json)

    print("Done!")


if __name__ == '__main__':
    main()
