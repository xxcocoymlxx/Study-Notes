'''
CSC263 Winter 2019
Problem Set 1 Starter Code
University of Toronto Mississauga
'''

# Do NOT add any "import" statements
def insert(sorted_list, number):
  '''
  Pre: sorted_list is a sorted list of numbers
  Post: return a sorted list with number in it
  '''  
  if len(sorted_list) == 0:
    return [number]
  if len(sorted_list) == 1:
    if sorted_list[0] > number:
      return [number, sorted_list[0]]
    elif sorted_list[0] < number:
      return [sorted_list[0], number]
    else:
      return [sorted_list[0], number]
  else:
    mid = len(sorted_list) // 2
    if number > sorted_list[:mid][-1]:
        return sorted_list[:mid] + insert(sorted_list[mid:], number)
    else:
      return insert(sorted_list[:mid], number) + sorted_list[mid:]


def get_min(sorted_list, count):
  '''
  Pre: sorted_list is a sorted list
  Post: return the count-th number in sorted_list
  '''  
  return sorted_list[count]



def solve_moving_min(commands):
  '''
  Pre: commands is a list of commands
  Post: return list of get_min results
  '''
  sorted_list = []
  final_list = []
  count = 0
  for command in commands:
    if command == "get_min":
      final_list.append(get_min(sorted_list, count))
      count += 1
    else:
      number = int(command.split()[1])
      sorted_list = insert(sorted_list, number)
  return final_list   


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