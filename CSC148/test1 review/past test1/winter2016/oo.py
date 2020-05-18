
class TaskOverloadError(Exception):
  pass

class InvalidDateError(Exception):
  pass

class ToDoList:

  def __init__(self, name, tasks):
    self.name = name
    self.tasks = tasks
    # Students don't have to prevent more than 50 tasks here
    
  def add_task(self, task):
    if len(self.tasks) >= 50:
      raise TaskOverloadError

    self.tasks.append(task)


class Task:

  def __init__(self, day, month, year, details):
    if (1 <= day <= 31 and 1 <= month <= 12 and year >= 2016):
      self.day = day
      self.month = month
      self.year = year
      self.details = details
    else:
      raise InvalidDateError


l = ToDoList("School", [])
day = input("please give day: ")
month = input("please give month: ")

try:
  t = Task(int(day), int(month), 2016, "Ace CSC148 test")
  l.add_task(t)
except InvalidDateError:
  print("invalid date")
except TaskOverloadError:
  print("too many tasks")
