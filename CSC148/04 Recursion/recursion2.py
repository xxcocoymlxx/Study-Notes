def sumlist(lst):
    '''
    (list of int) -> int
    lst is arbitrarily nested.
    Return the sum of lst.
    >>> sumlist([1,2,[3,[4]],5])
    15
    '''
    s = 0
    for elm in lst:
        if not isinstance(elm, list):
            s += elm
        else:
            s += sumlist(elm)#这个function就是用来算list里的sum的,算出sub-list里的sum
    return s

def flatten(lst):
  '''(list of int) -> list of int
  
  Print out all the elements in the list and its nested sub-lists.
  The given lst may contain nested lists, up to any depth.
  
  >>> flatten([2,9,[2,1,13,2],8,[2,6]])
  [2,9,2,1,13,2,8,2,6]

  >>> flatten([[9,[7,1,13,2],8],[7,6]])
  [9,7,1,13,2,8,7,6]
  
  >>> flatten([["this",["a",["thing"],"a"],"is"],["a","easy"]])
  ["this","a","thing","a","is","a","easy"]
  
  >>> flatten([])
  []
  '''
  new_lst = []
  for elm in lst:
      if not isinstance(elm, list):
          new_lst.append(elm)
      else:
          new_list.extend(flatten(elm))#注意extend的用意！！！
  return new_lst
        #flatten这个function会return一个list
    #所有我们要用extend只把sub-list里面的element加进去
    #(extend是用来取消掉一层list括号的)

#这里不能直接extend elm进去是因为不知道有几层nested list，
#若只有一层，那可以直接extend，但万一还有sub-list，
#就还要call这个function去handle


def count_odd(lst):
    '''
    Return the number of odd elements in the list.
    lst is arbritrarily nested.
    '''
    c = 0
    for elm in lst:
        if not isinstance(elm, list):
            if elm % 2 == 1:
                c += 1
        else:
            c += count_odd(elm)#算sub-list里面odd number的个数
            
    return c

def contains_odd(lst, num):
  '''
  (list of int) -> bool
  
  Given lst nested to arbitrary depth, return true iff the list contains
  at least num amount of odd numbers.
  '''

  return count_odd(lst) >= num


def swap_bottom(s):
  '''
  Swap the bottom two elements of Stack s.

  >>> s = Stack()
  >>> s.push(1)  --> bottom[1,2,3]top
  >>> s.push(2)
  >>> s.push(3)
  >>> swap_bottom(s)  --> bottom[2,1,3]top
  >>> s.pop()
  3
  >>> s.pop()
  1
  '''

  s2 = Stack()
  while not s.is_empty():
      s2.push(s.pop()) #s:[1,2,3]  s2:[3,2,1]
  first = s2.pop() #1
  second = s2.pop()#2
  s.push(second)
  s.push(first)
  while not s2.is_empty():
      s.push(s2.pop())#[2,1,3]


def rec_max(lst):
  '''(list of int, can be nested) -> int
  Return max number in possibly nested list of numbers.

  >>> rec_max([17, 21, 0])
  21
  >>> rec_max([17, [21, 24], 0])
  24
  '''
  nums = []
  for element in lst:
    if isinstance(element, int):
      nums.append(element)
    else:
      nums.append(rec_max(element))
  return max(nums)

  
def rec_max2(lst):
  '''(list of int) -> int
  Return max number in possibly nested list of numbers.

  >>> rec_max2([17, 21, 0])
  21
  >>> rec_max2([17, [21, 24], 0])
  24
  '''
  if lst == []:
    return float('-inf')#??????
  
  if isinstance(lst[0], int):
    return max(lst[0], rec_max2(lst[1:]))#comparing two numbers
  
  else:
    return max(rec_max2(lst[0]), rec_max2(lst[1:]))


def bin_search(lst, value):
  '''(list of int, int) -> bool

  Return True iff value is found in lst.
  Precondition: lst is sorted *the list should be divided in half
  to be more efficient.
  
  >>> bin_search([1, 3, 4, 5, 6], 6)
  True
  '''
  if len(lst) == 0:
    return False

  mid_index = len(lst)//2
  mid_value = lst[mid_index]

  if mid_value == value:
    return True
  elif mid_value < value:
    return bin_search(lst[mid_index+1:], value)
  else:
    return bin_search(lst[:mid_index], value)

