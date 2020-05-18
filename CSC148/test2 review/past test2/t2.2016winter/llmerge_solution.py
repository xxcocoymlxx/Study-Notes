class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.value) + " -> " + str(self.next)

def merge(lst1: Node, lst2: Node) -> None:
    
    lst1node = lst1
    lst2node = lst2
    
    while lst2node:
        rest = lst1node.next
        lst1node.next = Node(lst2node.value)
        lst1node.next.next = rest
        lst1node = rest
        lst2node = lst2node.next

a = Node(4)
a.next = Node(5)
a.next.next = Node(6)

b = Node(1)
b.next = Node(2)
b.next.next = Node(3)
b.next.next.next = Node(4)
b.next.next.next.next = Node(5)

merge(b,a)
print(b)
print(a)
