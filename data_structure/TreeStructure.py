class Node:
    def __init__(self,val):
        self.data=val
        self.right=self.left=None


def MorrisTraversal(root):
    # Set current to root of binary tree
    current = root

    while (current is not None):

        if current.left is None:
            print(current.data)
            current = current.right
        else:
            # Find the inorder predecessor of current
            pre = current.left
            while (pre.right is not None and pre.right != current):
                pre = pre.right

                # Make current as right child of its inorder predecessor
            if (pre.right is None):
                pre.right = current
                current = current.left

                # Revert the changes made in if part to restore the
            # original tree i.e., fix the right child of predecessor
            else:
                pre.right = None
                print(current.data)
                current = current.right
n=Node(1)
n.left=Node(2)
n.right=Node(3)

MorrisTraversal(n)