from partition_alt import partition

def quicksort(a: list, l: int, u: int) -> None:
  '''Sort the given list a in non-descending order.
  Precondition: 0 <= l and u < len(a)'''

  if l < u:
    mid = (l + u) // 2
    three = [a[l], a[mid], a[u]]#the median value among the first, the last, the middle elements is the pivot
    three.sort()
    if three[1] == a[l]:
      pivot_loc = a[l]
    elif three[1] == a[u]:
      pivot_loc = a[u]
    else:
      pivot_loc = a[mid]
   
    i = partition(a, l, u, pivot_loc)#i is a tuple 
    quicksort(a, l, i[0] - 1)#from the start to the last elm that is less than the pivot
    quicksort(a, i[1], u)#from the first elm that is greater than the pivot to the end
