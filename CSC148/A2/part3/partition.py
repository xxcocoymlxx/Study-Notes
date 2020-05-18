def partition (a: list, l: int, u: int, pivot: object) -> int:
  '''Rearrange list a so that elements >= pivot follow
  all elements < pivot. Return index of first element >= pivot.
  '''
  
  i = l
  j = l
  while j <= u:
    if a[j] < pivot:
      a[i], a[j] = a[j], a[i]
      i += 1
    j += 1
  return i
     
