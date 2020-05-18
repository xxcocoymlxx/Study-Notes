Handout, Question 1

class Node:
  
  def __init__(self, value):
    self.value = value
    self.next = None


a = Node(4)
a.next = Node(5)
b = Node(6)
c = a.next
c.next = b


The resulting list is:
4->5->6->None
Variable 'a' refers to the head of this list.


-----

Handout, Question 2

class Node:
  
  def __init__(self, value):
    self.value = value
    self.next = None
          
def mystery1(lnk): # purpose???
  while lnk and lnk.next:
    lnk.next = lnk.next.next
    lnk = lnk.next

Purpose of mystery1:

lnk is left with only the final element

lnk ends up with the final element or is empty.

lnk is left with only the third element.

If lnk has even number of elements, it ends up empty; if odd number of elements, only last element is left.

The above are all incorrect!

Correct ones:
Alternate between dropping and keeping the list elements. (OK, but not precise enough.)
Remove every element with an odd index. (Indexes aren't well-defined for linked lists...)

I would say that the next two are best:
Starting from the second element in linked list lnk, remove every other element.
Remove elements 2, 4, 6, 8, ... from the linked list lnk

  
def mystery2(lnk): # purpose???
  if not lnk:
    return
  lnk = lnk.next
  start = lnk
  while lnk and lnk.next:
    lnk.next = lnk.next.next
    lnk = lnk.next
  return start
  
What does mystery2 do:
Starting from the first element of linked list lnk,
remove every other element. Return the beginning of the linked list.

One final question: why doesn't mystery1 have a return, but mystery2 does???
#第二个是变成了2 4 6 8，return start， start就被重新赋值了新的linked list，1就直接不要了


-----

Handout, Question 3

The reverse function is correct! Take some time to understand it.
A few traces should help give you the intuition/insight into why it works.
