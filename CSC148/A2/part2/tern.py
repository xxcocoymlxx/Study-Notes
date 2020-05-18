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
      self.root.put(s + "$")
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
    children.'''
    
    self.key = key
    self.left = left
    self.centre = centre
    self.right = right

  def has_key(self, s: str) -> bool:
    '''Return True iff the tree rooted at this node contains the given string s.'''
    found = False
    
    if s[0] < self.key:
      if self.left:
        found = self.left.has_key(s)
        
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
      self.left.put(s)

    elif s[0] > self.key:
      if self.right == None:
        self.right = TreeNode(s[0])
      self.right.put(s)

    elif s != "$":#s[0] = self.key and s is not empty string（empty str cannot be added）
      if self.centre == None:
        self.centre = TreeNode(s[1])
      self.centre.put(s[1:])


  # TO DO: COMPLETE THIS METHOD
  def collect_sorted(self, curstring: str, sortlist: list) -> list:
    '''Return all the strings that are stored in the tree rooted at this node,
    in sorted (non-descending) order.
    sortlist is the list that you return at the end, so it is a list of all 
    the words in t in sorted order.
    curstring is how much of the string you read so far -- because in the tree,
     the nodes each store one character, so you will be reading the keys one 
     character at a time and updating curstring as you go.
    '''
    #the root exists
    if self.left == self.centre == self.right == None: #reached the end of a word that contains '$'
      sortlist.append(curstring) #we don't add the self.key (the '$') to curstring

    if self.left:
      self.left.collect_sorted(curstring,sortlist)

    if self.centre:
      self.centre.collect_sorted(curstring+self.key, sortlist)#only self.centre has the prefix of the word

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

