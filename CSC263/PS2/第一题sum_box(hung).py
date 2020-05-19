class Node:#Sum-box
    def __init__(self, key, s):
        self.key = key #(i, j)
        self.sub_sum = s #ai+a(i+1)+...+aj
        self.left = None
        self.right = None
        #self.parent = None



def partial_sum(S, m):
    if S.key[1] == m:
        return S.sub_sum

    elif (S.key[0]+S.key[1])//2 < m:
        return S.left.sub_sum + partial_sum(S.right, m)
    else:
        return partial_sum(S.left, m)

def change(S, i, y):
    if S.key[0] == S.key[1] == i:
        S.sub_sum = y
        return

    if (S.key[0]+S.key[1])//2 < i:
        change(S.right, i, y)#change ai to y
    else:
        change(S.left, i, y)

    S.sub_sum = S.left.sub_sum + S.right.sub_sum #update
    

    
    
