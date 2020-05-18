'''
               best    worst
quicksort      nlogn     n^2
merge          nlogn     nlogn
insertion       n         n^2
selection       n^2       n^2
bubble         n^2          n^2


'''
#quicksort, the worst-case running time of quicksort is still
#O(n^2), though on average it is O(n lg n)

l = [5,4,6,8,2,1,3,4,9,7,0]

#intro quicksort，不太正规的帮助理解的quicksort
def quicksort_0(l)-> list:
    '''把比我小的都放到我的前面，把比我大的都放到我的后面, 再用recursion处理两个sub list'''
    if len(l) < 2:#bace case，length是0或1的时候不用处理
        return l

    left = []
    right = []
    for i in range(1,len(l)):#这里是把list的第一位元素当做我，list其他元素都和我比较
        if l[0] < l[i]:
            right.append(l[i])
        else:
            left.append(l[i])

    return quicksort_0(left) + [l[0]] + quicksort_0(right)#recursion，返回一个完全sort好的list

#by Hung
def quicksort(l,start, end):
    '''start是初始index，end是结束index'''
    if start >= end:#因为下面i = start+1，并且i是一直在往上加的，一旦start超过了end就结束就行
        return
    
    pivot = l[start] #把list里第一位元素作为pivot
    i = start+1#从start后一位的元素开始比较
    while i != end+1: #直接拿pivot后一位和他比较，一直比较到list最后一位
        if pivot > l[i]:
            e = l.pop(i)
            l.insert(start,e) #start一直是起始index，这里也就是insert到了pivot的前面
        i += 1

    #上面那个loop结束以后所以比pivot小的元素就全部到pivot前面了，但pivot前面和后面的sublist的顺序还没有排好
    pivot_index = l.index(pivot)#用.index()method得到这个pivot的index
    #（因为比pivot小的元素全部被inset到了pivot前面，pivot不再是第一位）
    #此时pivot是在合适位置的，我们只需要对pivot前面和pivot后面的元素进行sort就好
    quicksort(l,start, pivot_index-1)#pivot_index-1就是pivot前一位，最后一位比pivot小的元素
    quicksort(l,pivot_index+1, end)#从第一位比pivot大的数到结尾开始sort
    return

#by slides
#We’re going to keep indices i and j, Stuff to the left of i is less than the pivot
#Stuff from i up to but not including j is greater or equal to the pivot
#Stuff from j to the right is unprocessed
def partition(lst, left, right, pivot):
'''(list, int, int, int) -> int
    left是given list起始index，right是given list结束index，pivot可以是个不在list里的元素
    Rearrange lst to【小于pivot的元素 |i| 大于等于pivot的元素 |j| unsorted 】
    return第一个大于等于pivot的元素的index，也就是i'''
    i = left#一开始i和j都是起始index
    j = left
    while j <= right:#j之后的元素都是unsorted的，while没到list末尾
        if lst[j] < pivot:
            lst[i], lst[j] = lst[j], lst[i]#把比pivot小的元素和前面第一位比pivot大的元素交换（i记录的一直是第一个比pivot大的元素）！大的元素交换到后面后还是一样的
            i += 1 #走到这里就有了一个比pivot小的元素，加1后，i就又是比pivot大的第一个元素，这是loop里的一部分，只要有比pivot小的元素i就会一直积攒积攒积攒
        j += 1#这一步才loop起来

    return i#i积攒到最后，i前面的所有元素就都是比pivot小的，i就是第一个比pivot大的元素的index

    #l = [5,4,6,8,2,1] pivot：3 left：0 right：5

def quicksort(lst, left, right):
'''(list, int, int) -> NoneType
    Sort lst[left..right] in nondecreasing order.'''
    if left < right:
        pivot = lst[right] #让list里最后一位元素做pivot
        i = partition(lst, left, right - 1, pivot) #最右边的元素做了pivot，所以我们从倒数第二位开始比较，这里的i就是第一位比pivot大的元素的index
        lst[i], lst[right] = lst[right], lst[i]#l = [1,2,4,5,6,8,3] pivot：3 此时i就是4（我们只是对第一位到倒数第二位的元素进行了排序）
        #这里4和3交换，pivot就到了合适的位置，4到了最后还是在比pivot大的sublist里
        quicksort(lst, left, i - 1)#然后再对比pivot小的sub list进行排序
        quicksort(lst, i + 1, right)#经过了交换pivot的位置，此时pivot已经在合适的位置，我们现在再对比pivot大的sub list进行排序就好

###########################################################################################################################

#merge sort
#intro的不正规的帮助理解的merge sort
def mergesort_0(l) ->list:
    '''不断的劈开劈开劈开，劈成单个元素，也就是先recursion，后操作，再两两比较，小的排前面，
    两个两个的里面的小的那个再互相比较，再把几个sublist按顺序merge起来。
    First divide the list into the smallest unit (1 element), 
    then compare each element with the adjacent list to sort 
    and 【merge】 the two adjacent lists. 
    Finally all the elements are sorted and merged.'''
    if len(l) < 2:#length是0或1
        return l

    left = mergesort_0(l[:len(l)//2])#得到了已经sort好的前一半元素
    right = mergesort_0(l[len(l)//2:])#得到了已经sort好的后一半元素

    new = []#再比较left和right里面的元素，按照大小顺序append进new里
    while left and right:#当left和right是相同长度时，如果不是相同长度，有一个已经为空list了，直接走到下面的extend
        if left[0] < right[0]:#每次比较两个list里的第一位元素，比较完后也pop第一位元素
            new.append(left.pop(0))
        else:
            new.append(right.pop(0))

    new.extend(left)#这里两个都往里面extend，因为如果是空list也没事
    new.extend(right)
    return new

#by Hung
def mergesort(l, start, end):
    '''start是起始index，end是length'''
    if start == end or start+1 == end:
        return
    
    mergesort(l, start, (start+end)//2)#注意！一定是(start+end)//2，而不是每次recursion都从头到尾的index除2，而是要得到当前index到结尾的中间index
    mergesort(l, (start+end)//2, end)#这里的recursion不断劈不断劈会一直劈到base case里的情况后，开始进入下面的code开始比较，一层一层返回sort过得list

    left = l[start:(start+end)//2]#left和right是l的复制！left此时已经是sort好的前半部分
    right = l[(start+end)//2:end]#right此时已经是sort好的后半部分

    i = start
    while left and right:
        if left[0] < right[0]:
            l[i] = left.pop(0)#直接把l里的元素重新赋值，就不用return新list，我们只是modify了这个list
        else:
            l[i] = right.pop(0)
        i += 1

    #上面的loop结束，说明left和right有一个为空了
    if left != []:
        while left:
            l[i] = left.pop(0)#此时的i还是上面loop结束时的最后一位modify过得元素的后一位元素的index
            i += 1#把left里剩下的所有元素都加进去
    else:#if right != []
        while right:
            l[i] = right.pop(0)
            i += 1
            

#by slides
def merge(list1, list2):
'''(list,list)->list
    mergesort的helper function
    Return merge of sorted list1 and list2. Merging Two Sorted Lists'
    把两个已经sort好的list按照顺序merge起来'''
    lst = []
    i=0#list1的起始index
    j=0#list2的起始index
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            lst.append(list1[i])
            i=i+1#记录比较过的元素的index，也loop循环起来
        else:
            lst.append(list2[j])
            j=j+1#记录比较过的元素的index，也让loop循环起来

    lst.extend(list1[i:])#再把loop结束以后还没有被比较过得元素全部放进新list里
    lst.extend(list2[j:])

    return lst

#mergesort by slides
from merge import merge

def mergesort(lst: list) -> list:
'''Return a sorted copy of lst.'''
    if len(lst) <= 1:
        return lst[:]
    mid = len(lst) // 2
    left = lst[:mid]
    right = lst[mid:]
    left_s = mergesort(left)
    right_s = mergesort(right)

    return merge(left_s, right_s)


####################################################################################################################################

#by Hung
def bubble(l):#O(n^2), They have an outer loop that runs n times，and an inner loop that runs n times
    '''[unsorted|sorted],given list里的元素两两比较，如果前一个元素比后一个元素大就交换位置，一个pass过后最大值就在list的最后.
        第一个loop是得到已经sort过得list的长度，真正操作是第二个loop，第二是loop每次只取到n-1，只要前一个比后一个大就交换，比较之后马上交换，在for里面比较次数是固定的
        最好情况是一次都不换，但还是要比较，最好情况的话只会比较n^2,最坏情况是每次都要换，比较和交换是并列动作，所以也是n^2
        如果最好情况是n，说明code写的不一样，做了优化，什么时候从头到尾都没有交换的时候，就是最好情况，只做了比较，没有交换，只有比较了需要交换才交换
        设了个flag为false，只要有任何一次交换发生了，flag就设为true。
        '''
    for i  in range(1, len(l)):#第一个loop只是为了得到已经sort过的元素数量
        for j in range(0,len(l)-i):#第二个loop得到0~总长度减去sorted部分，也就是我们要处理的部分
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]

#######################################################################################################
#by Hung
def insertion(l):#O(n^2)
    '''[sorted|unsorted]，将unsorted部分里的第一个元素插入到sorted部分合适的位置，一直往前看，比我大就一直往前走，直到走到比我小的数后面
        第一个for，默认前i位都排好顺序了，现在要把i+1位放到合适的位置去。合适的位置就是和前面的比较，只要前面的比我小，就换
        知道比我大的数为止，induction的思想。
        最坏情况：比较和交换是同级别的，比一次换一次，比较和交换都是在第二个loop里，所以是n^2，前面有多长就要交换多少次
        最好情况：我的第i+1位已经比第i位大，这时直接终止for循环，因为我知道我的前i位是已经排好顺序的，如果i+1位比i位也大，那就已经在合适位置了，比较了一次，交换了0次
        外面的loop一共n次，如果每一层下面都只执行一次，那就是O（n）'''
    for i in range(0, len(l)):#第一个loop得到已经sort过得元素数量，第二个loop得到unsorted部分，也就是我们要处理的部分
        for j in range(i,0,-1):#从i到0，每隔-1个，也就是倒着回去，让最后的那个放到合适的位置去
            if l[j] < l[j-1]:
                l[j], l[j-1] = l[j-1], l[j]

#by slides
def insert(L, i):
'''(list, int) -> NoneType
    Move L[i] to where it belongs in L[:i].'''
    v = L[i]#不处理第一个元素，直接从第二个以第一个为标准开始处理
    while i > 0 and L[i - 1] > v:#一定前一位要小于后一位才做交换
        L[i] = L[i - 1]
        i -= 1

    L[i] = v#从上面那个loop出来了，就说明已经在合适位置了

def insertion_sort(L):
'''(list) -> NoneType
    Sort the elements of L in non-descending order.'''
    for i in range(1, len(L)):
        insert(L, i)

lst = [6, 2, 12, 6, 10, 15, 2, 13]
####################################################################################################
#by Hung
def selection(l):#O(n^2),They have an outer loop that runs n times
    '''[sorted|unsorted]，在unsorted部分里的最小元素和unsorted部分的第一个元素交换，也就是把最小的元素按顺序放到最前面
        无论是最好情况还是最坏情况都会做交换，排好的还是没排好的都是一样的
        在n个东西里找最小的至少比较n-1次，第一次n次，第二次n-1次，第三次n-3次，等差数列，
        比较n^2次，交换n次，他们平级，所以还是n^2'''
    for i in range(len(l)):
        min_index = i
        min_value = l[i]
        for j in range(i, len(l)):#i前面的就都是sorted的了，在unsorted里找min_value就行
            if l[j] < min_value:
                min_value = l[j]
                min_index = j#这个loop只是为了找到min value

        l[i], l[min_index] = l[min_index], l[i]#外面的for loop，交换n次


#by slides    
def find_min(L, i):
    '''(list, int) -> int
    Return the index of the smallest item in L[i:].'''
    smallest_index = i#初始index就是要找的list的第一位元素
    for j in range(i + 1, len(L)):
        if L[j] < L[smallest_index]:
            smallest_index = j#就在剩下的list里找比第一位元素小的元素，如果有就更新smallest_index
    return smallest_index

def selection_sort(L):
    '''(list) -> NoneType
    Sort the elements of L in non-descending order.'''
    for i in range(len(L) - 1):
        smallest_index = find_min(L, i)
        L[smallest_index], L[i] = L[i], L[smallest_index]
