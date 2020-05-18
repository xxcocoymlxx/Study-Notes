#不带壳的linked list，用recursion操作的reverse
    def reverse(self):
        '''Reverse the linked list.
            1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1
            原本的linked list [ 1 2 3 4 ] 直接被更改3和4之间的连接，3被连接到4后面去(4是不动的)
            所有链接全部倒转过去，一层一层叠代，从而变成 [4 3 2 1]
            看不懂的时候就画个图。
            head_node的值每次叠代分别是4，43，432，最后return 4321
            要相信self.next.reverse()是已经得到了next剩下所有已经reverse过得linked list'''
        if self.next == None:
            return self
            #注意！这里我们只return self而不是self.data
            #因为reverse后还是个linked list，要以node的形式return

        head_node = self.next.reverse()#在第三层recursion，探到了底，head_node里抓到了4，返回到上层recursion，上层recursion的self就是3
        self.next.next = self#此时的self就是3，self.next.next就是4的后面，等于了self，也就是3
        #【注意！我们只是断开了左边3和4之间的连接，但左边的2此时还连接着右边的3！】
        #所以左边的2的next还是右边的3，左边2的next的next就变成了右边的3的后面
        #所以assign 当前self左边的的2去self.next.next就是把2重新放去了右边3的后面！
        self.next = None#同时断开了原本3与4之间的连接，此时head_node就是4 3，然后返回到再上层recursion

        #这是创建了个new node的方法，以上的方法只是改变了linked list，没有创建新的node
        #head_node.append_node(self.data) 

        #每次recursion完成后都return了一个head_node作为上一层recursion的抓到的值
        #当所有recursion完成后，才最终return reversed过的linked list，也就是head_node
        return head_node

        #新的理解
        #head_node = self.next.reverse()此时head_node就是已经reverse好的432，self就是1
        #self.next.next = self#此时的self.next就是432！！self.next.next就是432的后面，让他跟上1！
        #self.next = None


    def reverse1(self):
        '''l = 1 2 3 4, l points to 1, after reverse, 4 3 2 1, but l still points to 1'''
        if self.next == None:
            return self

        new = self.next.reverse1() #此时new就是432

        curr = new #这里就是432的头结点，4
        while curr.next != None:
            curr = curr.next#找到432的最后一位了

        curr.next = self #让432的最后一位跟上1
        self.next = None# 断开链接

        return new
        

#带壳的linked list，用loop操作的reverse
    def reverse(self):
        '''Reverse the linked list. 不用recursion写，用loop写。
            [1 2 3]这个例子的话，
            第一次loop，让1后面接上了head的值（此时为None），并且断开了1和2之间的链接，同时assign新的head值，也就是当前curr和后面跟着的值，[1 None]
            第二次loop，让2后面跟上了head的值（此时为1，而1通过第一次loop后面又跟着None），并且断开了2和3之间的链接，同时assign新的head值,[2 1 None]
            第三次loop，让3后面跟上了head的值（此时为2，2后面跟着1，1后面跟着None），[3 2 1 None]
            head是每loop一次都是在不断累积新的值的，从让None跟着第一个元素，让第二个元素跟上第一个元素和None，依次累积。
            一定要画图理解！！'''
        if self.head == None:
            return

        head = None#初始head为None，是为了让linked list里第一个值后面接上None，后面head的值也在不断刷新
        curr = self.head
        while curr != None:
            curr_next = curr.next#一定要在这里先存一个curr.next因为之后curr就会重新赋值，curr.next就变了！现在存的1.next就是2，一会儿1.next就是None了！！！！
            curr.next = head#把新的head的值跟到curr后面，并断开之间的链接
            head = curr#之前的head已经用完，此处刷新head的值，此时的head是跟了一串东西的一个node
            curr = curr_next##curr等于之前存的还没变过得下一个我们要reverse的元素，而不是我们后来添加到curr后面的元素
            
        #此时一定要重新assign self.head的值，不然self.head的值还是之前的！！
        self.head = head#当loop进不去说明curr已经是None，已经loop完了整个linked list
        #此时的head就是连着一大串元素的最后一个元素了，所以我们重新assign self.head为当前head，就完成了reverse linked list