'''
CSC263 Winter 2019
Problem Set 4 Starter Code
University of Toronto Mississauga
'''

# Do NOT add any "import" statements

class NodeQueue():
      
      def __init__(self):
            self.head = None
            self.end = None
            self.length = 0
            
            
            
      def enqueue(self, node):
            if self.head == None:
                  self.head = node
                  self.end = node
                  self.length = 1
            else:
                  self.end.next = node
                  self.end = node
                  self.length += 1
      
      
      def dequeue(self):
            if self.length == 1:
                  result = self.head
                  self.head = None
                  self.end = None
                  self.length = 0
                  return result
            else:
                  result = self.head
                  self.head = self.head.next
                  self.length -= 1
                  return result




class Node():
  
      def __init__(self, data):
            self.data =  data
            self.next = None
            self.distance = 0
            self.checked = False
            self.connected = [] #和他不在一个party的所有other nodes
            
            
      def __repr__(self):
            result = ""
            result += self.data + "["
            for node in self.connected:
                  result += node.data
            result += "]"
            return result
    

                        



def generate_graph(node_num1, node_num2, diction):
      if node_num1 in diction.keys():#如果第一个学生在list里
            if node_num2 in diction.keys():#第二个学生也在list里
                  #互相加到对方的“不在同一个party”的list里
                  diction[node_num1].connected.append(diction[node_num2])
                  diction[node_num2].connected.append(diction[node_num1])
            else:#如果第一个学生在list里而第二个学生不在
                  new_node = Node(node_num2)#为第二个学生创建一个新的node
                  new_node.connected.append(diction[node_num1])#把第一个学生加到第二个学生的list里
                  diction[node_num2] = new_node#把第二个学生加进graph里
                  diction[node_num1].connected.append(new_node)#把第二个学生加到第一个学生的list里
      else:#if node_num1 不在adjacency list里
            if node_num2 in diction.keys():#而第二个学生在graph里
                  new_node = Node(node_num1)#就为第一个学生新建一个node
                  new_node.connected.append(diction[node_num2])
                  diction[node_num1] = new_node
                  diction[node_num2].connected.append(new_node)#一样的操作，互相加进list
            else:#如果两个学生都不在graph里，就都新建一个node并放进graph里和互相成为”不在一个party“里的人
                  new_node1 = Node(node_num1)
                  new_node2 = Node(node_num2)
                  new_node1.connected.append(new_node2)
                  new_node2.connected.append(new_node1)
                  diction[node_num1] = new_node1
                  diction[node_num2] = new_node2
                  
                  





def get_path(node1, node2):
      '''用Queue的基本上是个BFS，用来找shortest path'''
      if node1 == node2:
            return -1
      Node_queue = NodeQueue()
      Node_queue.enqueue(node1)
      node1.checked = True
      while Node_queue.length != 0:
            node = Node_queue.dequeue()
            for nodes in node.connected:
                  if nodes.checked == False:
                        nodes.checked = True
                        #the self.distance of this node will be the distance of 
                        #the node who finds the current node + 1.
                        #basically有几层这里就加几
                        nodes.distance = node.distance + 1
                        if nodes.data == node2.data:
                              return nodes.distance
                        Node_queue.enqueue(nodes)
      return 0




def solve_party(commands):
      '''
      Pre: commands is a list of commands
      Post: return list of 'tell' results
      '''
      graph = {}#a dictionary that works as an adjacency list
      result = []
      
      for command in commands:
            if command[0] == 't':
                  node_num1 = command.split()[-2]
                  node_num2 = command.split()[-1]
                  if not (node_num1 in graph.keys() and node_num2 in graph.keys()):
                        result.append('unknown')

                  else:
                        num = get_path(graph[node_num1], graph[node_num2])
                        if num == 0:
                              result.append('unknown')
                        elif num == -1 or num%2 == 0:
                              result.append('same')
                        elif num%2 == 1:
                              result.append('different')
                        for key in graph:
                              graph[key].checked = False
                              graph[key].next = None
                              graph[key].distance = 0
            if command[0] == 'a':
                  node_num1 = command.split()[-2]#得到倒数第二个数
                  node_num2 = command.split()[-1]#得到倒数第一个数
                  generate_graph(node_num1, node_num2, graph)#每次add就添加一个edge到graph里
      return result
      
      
  

if __name__ == '__main__':

      # some small test cases
      # Case 1
      assert ['unknown', 'different', 'same'] == solve_party(
      ['tell 1 3',
       'add 1 3',
       'tell 1 3',
       'add 3 4',
       'tell 1 4'
       ])
