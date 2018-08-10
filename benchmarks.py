import json
import re

from statistics import median


def json_loads_test():
    with open("test.json", "r") as file:
        json.loads(file.read())


def aggregation_from_dict_test(data):
    for i in range(10):
        from_values = [int(feature["properties"]["FROM_ST"]) for feature in data["features"] if
                       feature["properties"]["FROM_ST"] is not None]
        to_values = [int(feature["properties"]["TO_ST"]) for feature in data["features"] if
                     feature["properties"]["TO_ST"] is not None]
        result = [from_values[i] * to_values[i] for i in range(len(from_values))]
        median(result)


def regexp_test(string):
    re.findall("[+-]?\d+(?:\.\d+)?", string)
