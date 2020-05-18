def partition (a: list, l: int, u: int, pivot: object) -> 'tuple of two ints':
  '''Alternate partition: This new partition procedure maintains two
  split points, dividing the list into those elements that are smaller
  than the pivot, those exactly equal to the pivot, and those strictly
  larger than the pivot. Return a tuple of the indices of the two split points.

  >>> l = [-19, 1, 1, 1, 18, 18, 104, 418]
  >>> partition(l, 0, len(l)-1, 18)
  (4, 6)
  >>> l
  [-19, 1, 1, 1, 18, 18, 418, 104]
  '''
  
  i = l
  j = l
  k = u
  while j <= k:#注意！这里j<= k，k是比pivot大的元素的队列的前一位元素，k以后的元素相当于都是sort过的比pivot大的元素，所以j不用处理k以后的元素
    if a[j] < pivot:
      a[i], a[j] = a[j], a[i]#遇到了比pivot小的元素就放到i的位置(比pivot小的队列里)，同时i向后移一位
      i += 1#为了记录比pivot小的元素的个数，i就是比pivot小的最后一个元素的后一个数
      j += 1#为了循环起来
    elif a[j] == pivot:
      j += 1#为了循环起来，和pivot一样大的元素就放着不管，继续循环
    else:#if a[j] > pivot
      a[j], a[k] = a[k], a[j]#遇到了比pivot大的元素就放到比pivot大的元素的队列里，同时k向前移一位，同时k本来的元素被提上前来处理
      k -= 1#为了倒着记录比pivot大的元素的个数，k就是比pivot大的元素的队列的前一位元素
  return (i, j)#最终i就是比pivot小的最后一个元素的后一个数，也就是跟pivot一样大的第一个元素的index
               #最终j就是第一个比pivot大的数
