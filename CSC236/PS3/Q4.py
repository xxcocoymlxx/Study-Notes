'''
def social_distance(prefa, prefb):
    acc1 = {}
    acc2 = []
    num = 0
    for i in range(len(prefa)):
        acc1[prefa[i]] = i
    for j in prefb:
        acc2.append(acc1[j])
    for n in range(len(acc2)):
        for m in acc2[n+1:]:
            if acc2[n] > m:
                num += 1
    return num
    '''
#########################################################################################

#2T(n/2)+nlogn + 2n

#n
def social_distance(prefa, prefb):
    ranka = {}
    for i in range(len(prefa)):
        ranka[prefa[i]] = i

    rankb = []
    for j in prefb:
        rankb.append(ranka[j])
        
    return distance(rankb)

#nlogn
def comb(lst1,lst2):
    comb_num = 0
    sort_lst1 = lst1
    sort_lst2 = lst2
    sort_lst1.sort()
    sort_lst2.sort()
    x = 0
    y = 0
    while x < len(sort_lst1) and y < len(sort_lst2):
        if sort_lst1[x] > sort_lst2[y]:
            comb_num += len(sort_lst1)
            y += 1
        else:
            x += 1
    return comb_num

#2T(n/2)+nlogn
def distance(rankb):
    if len(rankb) <= 1: #base case1
        return 0
    elif len(rankb) == 2:#base case2
        if rankb[0] > rankb[1]:
            return 1
        else:
            return 0
    else:
        mid = len(rankb)//2
        left = rankb[0:mid]
        right = rankb[mid:]
        return distance(left) + distance(right) + comb(left,right)



    
    
    
                
             
