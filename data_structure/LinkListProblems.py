class ListNode:

    def __init__(self, x):
        self.val = x
        self.next = None


def printNode(head) -> ListNode:
    n = head
    nodes = ""
    while n is not None:
        nodes = nodes + "-->" + str(n.val)
        n = n.next
    print(nodes)


import heapq


def merge_nodes(lists: list[ListNode]) -> ListNode:
    if len(list) == 0:
        print("Nodes empty")
        return
    for n in list:
        print()



if __name__ == "__main__":
    n = ListNode(1)
    n.next = ListNode(2)
    printNode(n)
