#Java is also  similar
def subset_sum(numbers, target, partial=[]):
    s = sum(partial)  # find the sum from sublist

    # check if the partial sum is equals to target
    if s == target:
        print("sum(%s)=%s" % (partial, target))
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]  # getting the 1st/i th  element from the list/array
        remaining = numbers[i + 1:]  # Add the remaining all the elements to temp list
        subset_sum(remaining, target, partial + [n])  # Recursive call:::with remaining list,target,partial=(subset
        # from the original list of (ith elements on each iterations  )


arr = [1,2,3,4,5,6,7,8,9,-11]
n = 10
sorted()
subset_sum(arr, n, [])

#output
'''
sum([1, 2, 3, 4])=10
sum([1, 2, 7])=10
sum([1, 3, 6])=10
sum([1, 4, 5])=10
sum([1, 9])=10
sum([2, 3, 5])=10
sum([2, 8])=10
sum([3, 7])=10
sum([4, 6])=10
'''

