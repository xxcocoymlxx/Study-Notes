class TernarySearchTree:

  def __init__ (self) -> None:
    '''Create an empty TernarySearchTree.'''
    
    self.root = None

  def has_key(self, s:str) -> bool:#their helper functions in TreeNode class is different
    '''Return True iff this tree contains the given string s.'''
    
    if self.root:
      return self.root.has_key(s + "$")
    else:
      return False

  def has_key2(self, s:str) -> bool:
    '''???'''
    
    if self.root:
      return self.root.has_key2(s + "$")
    else:
      return False

  def put(self, s:str) -> None:
    '''Add in the given string s to the tree. Use the $ character
    to signify the end of a word.'''
    
    if self.root:
      self.root.put(s + "$")#每个单词的结尾都有个"$"！遇到有"$"就说明一个单词结束了！
    else:
      newkey = s + "$"
      
      # split apart the first character and add it to the root
      self.root = TreeNode(newkey[0])
      
      # put the rest of the string in, starting from this new root
      self.root.put(newkey)

  def collect_sorted(self) -> list:
    '''Return a list of all the words in this tree, in sorted order.'''
    
    if self.root:
      return self.root.collect_sorted("", [])

  def __repr__(self) -> str:
    '''Return string representation of this tree.'''
    
    return repr(self.root)

class TreeNode:
  '''A Tree node.'''
  
  def __init__(self, key: str, left: 'TreeNode' = None,
               centre: 'TreeNode' = None, right: 'TreeNode' = None) -> None:
    '''Create Tree node with the given key, and left, centre and right
    children.至于和key只能和centre组成词或者centre的左右孩子，key不能和自己的左右孩子组成词'''
    
    self.key = key
    self.left = left
    self.centre = centre
    self.right = right

  def has_key(self, s: str) -> bool:
    '''Return True iff the tree rooted at this node contains the given string s.'''
    #在ternaryTree的class里已经判断过root存不存在的问题了，所以都是默认root存在的
    #注意，这里放进来的s都是含有'$'的
    found = False
    
    if s[0] < self.key:
      if self.left:
        found = self.left.has_key(s)#小于key，那就说明不等于key，就在左支里带完整的string继续找
        
    elif s[0] > self.key:
      if self.right:
        found = self.right.has_key(s)

    else: # this means self.key == s[0]
      if s == "$": # we have reached end of the word
        found = True
      if self.centre: # the centre branch represents continuation of this word
        found = self.centre.has_key(s[1:]) # so we search for rest of the word along this branch

    return found

  def has_key2(self, s):
    '''returns True when it is an empty string and
       part of the string (first few letters of the string)
       is found in the tree.'''
    if s == "$":
      return True
    if s[0] < self.key:
      if self.left:
        return self.left.has_key2(s)
      else:
        return False
    elif s[0] > self.key:
      if self.right:
        return self.right.has_key2(s)
      else:
        return False
    else:#if s[0] = self.key
      if self.centre:
        return self.centre.has_key2(s[1:])
      else:
        return False

  def put(self, s):
    '''Add the given string s to the tree rooted at this node.'''

    if s[0] < self.key:
      if self.left == None:
        self.left = TreeNode(s[0])
      self.left.put(s)#一直在缩短s的规模，每套一次recursion都是砍一次

    elif s[0] > self.key:
      if self.right == None:
        self.right = TreeNode(s[0])
      self.right.put(s)

    elif s != "$":#进不去前两个if那只可能s[0] = self.key and s is not empty string（empty str是加不进去的）
      if self.centre == None:
        self.centre = TreeNode(s[1])
      self.centre.put(s[1:])


  # TO DO: COMPLETE THIS METHOD
  def collect_sorted(self, curstring: str, sortlist: list) -> list:
    '''Return all the strings that are stored in the tree rooted at this node,
    in sorted (non-descending) order.
    This method should create and return an alphabetically sorted list 
    consisting of exactly those strings represented in the ternary search tree. 
    you should collect the strings from the tree in sorted order; 
    you should NOT sort them afterwards as a separate step.
    按照左中右（从小到大的alphabetical order排列的）inorder遍历一遍，放进list。
    【sortlist】 is the list that you return at the end, so it is a list of all 
    the words in t in sorted order
    【curstring】 is how much of the string you read so far -- because in the tree,
     the nodes each store one character, so you will be reading the keys one 
     character at a time and updating curstring as you go
     他的每个node上都是一个字母，不能直接append进list，要放进string里，等一个完整的词累计好了以后才放到list里
     注意！他并不是遇到$就是一个词的结尾，每个path上只能有一个词，所以判断词的结束的依据是他是不是叶子！最后不要把$放进string里就好
    '''
    #以下的都默认有root
    if self.left == self.centre == self.right == None: #找到一个带$的完整的词
      sortlist.append(curstring)#此时的curstring就是累计好了这支上的所有字母的string，这里就不加self.key了，此时的self.key就是$

    if self.left:
      self.left.collect_sorted(curstring,sortlist)

    if self.centre:
      self.centre.collect_sorted(curstring+self.key, sortlist)#我试过self.key+curstring，出来的词是反的

    if self.right:
      self.right.collect_sorted(curstring,sortlist)

    return sortlist

  def __repr__(self) -> str:
    '''Represent this node as a string.'''
    
    return ('(' + str(self.key) + ', ' + repr(self.left) +
                ', ' + repr(self.centre) + ', ' + repr(self.right) + ')') 

t = TernarySearchTree()
t.put("hello")
t.put("help")
t.put("ok")
