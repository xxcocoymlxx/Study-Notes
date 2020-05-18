def get_common(s1,s2):
    i = 0
    word = ''
    
    while i < len(s1):
        
        if s1[i].upper() == s2[i].upper():
            new = s1[i].upper()
            word = word + new
            i += 1
        else:
            word = word + '_'
            i += 1
    return word
            
def convert_to_integer(counts):
    new_lst = []
    i = 0
    while i < len(counts):
        new_num = int(counts[i])
        new_lst.append(new_num)
        i += 1
    return new_lst



DISCOUNT1 = 0.10
DISCOUNT2 = 0.20
def apply_discount(dollar):
    if dollar <= 50:
        return dollar
    elif 50<= dollar and dollar <= 100:
        return dollar * (1-DISCOUNT1)
    else:
        return dollar * (1-DISCOUNT2)


def sort_correspnding(s1,s2):
    word1 = ''
    word2 = ''
    i = 0
    while i < len(s1):
        if s1[i] == s2[i]:
            word1 = word1 + s1[i]
            i += 1
        elif s1[i] != s2[i]:
            word2 = word2 +s1[i]
            i += 1
    return  (word1,word2)


def does_not_contain_char(s1,s2):
    i = 0
    while i < len(s2):
        if s2[i] in s1:
            return False
        else:
            return True
    i += 1


def cooking_time(num_potatoes,extra_large):
        if extra_large == True:
            if num_potatoes >=2:
                return num_potatoes * 7 - 3
            else:
                return num_potatoes * 7
        elif extra_large == False:
            if num_potatoes >=2:
                return num_potatoes * 5 - 3
            else:
                return num_potatoes * 5


def encrypt_word(word,key):

    '''
    no discribtion
    '''
    pass




HIDDEN = '^'
def merge_views(view1,view2):

    pass





letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def encrypt_letter(letter,num_key):
    new_index = 0
    if len(letter) == 1:
        if letter in letters:
            new_index = letters.index(letter)
            if new_index + num_key <= 26:
                return letters[new_index + num_key]
            elif new_index + num_key >= 26 :
                new_index = 26 - letters.index(letter)
                num_key = num_key - new_index
                return letters[num_key]



def pothole_to_camel(pothole):
    i = 0
    word = ''
    while i < len(pothole):
        if pothole[i] != '_':
            word += pothole[i]
            i += 1
        elif pothole[i] == '_':
            word += pothole[i+1].upper()
            i += 2
    return word
        
        

def new_math_test(old_test,operators):
    i = 0
    new_test = ''
    while i < len(old_test):
        if old_test[i].isdigit():
            new_test += " "
            i += 1
        elif old_test[i] in operators:
            new_test += '_'
            i += 1
        else:
            new_test += old_test[i]
            i += 1
    return new_test



def change_elements(lst,change):
    i = 0
    while i < len(change):
        if change[i] == True:
            lst[i] = 99
            i += 1
        else:
            lst[i] = lst[i]
            i += 1


def corrupted_text(corrupt,clean_up):
    i = 0
    abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLEMNOPQRSTUVWXYZ"
    word = ''
    while i < len(corrupt):
        if corrupt[i] in clean_up:
            word += '*'
            i += 1
        elif corrupt[i].isdigit() or corrupt[i] == ' ' or corrupt[i] in abc:
            word += corrupt[i]
            i += 1
        else:
            word += ' '
            i += 1
    return word


def auction_average(player1_bids,player2_bids):
    pass



def election_results(party1_votes,party2_votes):
    pass



def greater_than(s,d):
    i = 0
    while i < len(s):
        if int(s[i]) > d:
            return True
        else:
            i += 1
    return False
        
            
def bouns_amount(num_sold):
    if num_sold <10:
        return 0
    elif num_sold >10 and num_sold<15:
        return 100
    else:
        return 200

def sort_letters(s1,s2):
    pass


def num_before(lst):
    for item in lst:
        if item == 99:
            return int(item[0] - 1)
        else:
            return len(lst)


#last page#

def make_absolute(nums):
    new_lst = []
    for item in nums:
        new_lst.append(abs(item))
    return new_lst












    
    






