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


def quick_sort_test(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
        less = quick_sort_test(less)
        more = quick_sort_test(more)
        return less + pivotList + more


def merge(l, p, q, r):
    n1 = q - p + 1
    n2 = r - q
    left = l[p: p + n1]
    right = l[q + 1: q + 1 + n2]

    i = 0
    j = 0
    k = p
    while k < r + 1:
        if i == n1:
            l[k] = right[j]
            j += 1
        elif j == n2:
            l[k] = left[i]
            i += 1
        elif left[i] <= right[j]:
            l[k] = left[i]
            i += 1
        else:
            l[k] = right[j]
            j += 1
        k += 1


def _merge_sort(l, p, r):
    if p < r:
        q = int((p + r) / 2)
        _merge_sort(l, p, q)
        _merge_sort(l, q + 1, r)
        merge(l, p, q, r)


def merge_sort(l):
    _merge_sort(l, 0, len(l) - 1)


class BinaryTreeNode:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BinaryTreeNode(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BinaryTreeNode(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data


def binarytree_test():
    tree = BinaryTreeNode(data=0)
    for i in range(1, 10000):
        tree.insert(i)
