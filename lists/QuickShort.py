'''
Algo
-------------
quick_short(arr[],low,high)
if(low<high)
partition is partitioning index, arr[p] is now at right place
partition=partition(arr[],low,high)
 quickSort(arr, low, pi - 1);  // Before partition
        quickSort(arr, pi + 1, high); // After partition
'''


def partition(arr,low,high):
    i=low-1
    pivot=arr[high]
    for j in range(low,high):
        if arr[j]<=pivot:
            i=i+1
            arr[i] ,arr[j]=arr[j], arr[i]
    arr[i+1],arr[high]=arr[high],arr[i+1]
    return i+1


def quick_short(arr,low,high):
    if low<high:
        p=partition(arr,low,high)
        quick_short(arr,low,p-1)
        quick_short(arr,p+1,high)




if __name__=='__main__':
    arr=[2,1,4,5,1,6,8,9,0,3,10,9]
    quick_short(arr,0,len(arr)-1)
    print(arr)



