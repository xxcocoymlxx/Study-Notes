'''
CSC263 Winter 2019
Problem Set 1 Starter Code
University of Toronto Mississauga
'''

# Do NOT add any "import" statements



def solve_moving_min(commands):
  '''
  Pre: commands is a list of commands
  Post: return list of get_min results
  '''
  # TODO: implement this function
  min_num = 0
  datas = []
  min_list = []

  for c in commands:
    if c == 'get_min':
      min_list.append(datas[min_num])
      min_num += 1

    else:
      n = int(c.split()[1])
      #datas = bst_list(n, datas)
      bst_list_no_return(n, datas,0,len(datas))

  return min_list
      


def bst_list(n,l):
  if l == []:
    return [n]
  if len(l) == 1:
    if n < l[0]:
      return [n,l[0]]
    
    return [l[0], n]
  
  mid = l[len(l)//2]

  if n < mid:
    return bst_list(n,l[:len(l)//2]) + l[len(l)//2:]

  else:
    return l[:len(l)//2] + bst_list(n,l[len(l)//2:])
    

def bst_list_no_return(n,l,s,e):
  if s == e:
    l.insert(s, n)
    return

  if s+1 == e:
    if n < l[s]:
      l.insert(s, n)
    else:
      l.insert(e, n)
    return

  mid_index = (s+e)//2

  if n < l[mid_index]:
    bst_list_no_return(n,l,s,mid_index)

  else:
    bst_list_no_return(n,l,mid_index,e)
  

    

if __name__ == '__main__':

    # some small test cases
    # Case 1
  assert [10, 5, 10] == solve_moving_min(
    ['insert 10',
     'get_min',
     'insert 5',
     'insert 2',
     'insert 50',
     'get_min',
     'get_min',
     'insert -5'
    ])
