import itertools
from typing import List


def find_pairs_from_array(arr, target):
    search_value = set()
    if len(arr) == 0:
        return []
    for i in arr:
        if target - i in search_value:
            print("Sum of (" + str(i) + "+" + str(target - i) + ")=" + str(target))
        else:
            search_value.add(i)


def find_pairs_from_array_2(arr, target):
    print("find_pairs_from_array_2")
    sum_array = {}
    if len(arr) == 0:
        return []
    from collections import Counter
    counter = Counter(arr)
    for i in arr:
        if counter.get(target - i) is not None:
            print("Sum of (" + str(i) + "+" + str(target - i) + ")=" + str(target))
            sum_array[str(i) + "+" + str(target - i)] = target
    if len(sum_array) == 0:
        print("No pairs avaliable")
    else:
        print(sum_array)


def find_pair_sum_if_array_is_sorted(arr: List, target: int):
    if len(arr) == 0:
        return
    result = []
    arr.sort()
    high = len(arr) - 1
    low = 0
    while low < high:
        sum = arr[low] + arr[high]
        if sum == target:
            result.append([arr[low], arr[high]])
            high -= 1
            low += 1
        elif sum < target:
            low += 1
        else:
            high -= 1


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 10
find_pairs_from_array(arr, target)
# find_pairs_from_array_2(arr, target)
