import random

def calc_new_fav(fave_number):
    '''
    (int) -> int

    Given a integer, return a new number after the caiculations.

    >>>calc_new_fav(0)
    123456

    >>>calc_new_fav(1)
    124480

    >>>calc_new_fav(20)
    3276923456
    '''
    return (((fave_number + fave_number) * 2) ** 5) + 123456

def div_by_5 (new_fave):
    '''
    (int) -> NoneType
    
    Given a new favorite number, print whether or not the given number is divisible by 5.
    
    >>>div_by_5 (0)
    Is new fave number divisible by 5? True

    >>>div_by_5 (1)
    Is new fave number divisible by 5? False

    >>>div_by_5 (20)
    Is new fave number divisible by 5? True
    '''
    if (new_fave % 5 == 0):
        print ("Is new fave number divisible by 5? True")
    else:
        print ("Is new fave number divisible by 5? False")
        
def div_by_5_num2 (new_fave_2):
    '''
    (int) -> NoneType

    Given another favorite number,  print whether or not the given number is divisible by 5.

    >>>div_by_5_num2 (0)
    Is new fave number divisible by 5? True

    >>>div_by_5_num2 (1)
    Is new fave number #2 divisible by 5? False

    >>>div_by_5_num2 (5688097)
    Is new fave number #2 divisible by 5? False
    '''
    if (new_fave_2 % 5 == 0):
        print ("Is new fave number #2 divisible by 5? True")
    else:
        print ("Is new fave number #2 divisible by 5? False"
               
def add_bob (fave_word):
    '''
    (str) -> str

    Given a favorite word, return a string after adding "World" and a random number of "Bob" to it.

    >>>add_bob (hello)
    helloworldbobob

    >>>add_bob (csc108)
    csc108worldbobbobbob

    >>>add_bob (catz)
    catzworldbobbob
    '''
    fave_word += "world"
    rand_num = random.randint(0,3)
    if rand_num == 0:
        fave_word += ''
    elif rand_num == 1:
        fave_word += 'Bob'
    elif rand_num == 2:
        fave_word += 'BobBob'
    elif rand_num == 3:
        fave_word += 'BobBobBob'
    else:
        fave_word += ''
    print(fave_word)


fave_number = 1
# doing some calculations on this number
print(calc_new_fav(fave_number))
               
# check if new_fave is divisible by 5
div_by_5 (calc_new_fav(fave_number))
               
fave_number_2 = 42
# doing the same calculations as above on this number
print(calc_new_fav(fave_number_2))
               
# check if new_fave_2 is divisible by 5
div_by_5_num2 (calc_new_fav(fave_number_2))
               
fave_word = 'hello'
# add 'world' and a random number (between 0-3) of 'Bob's to this word
print(add_bob (fave_word))
               
fave_word_2 = 'csc108'
# add 'world' and a random number (between 0-3) of 'Bob's to this word
print(add_bob (fave_word_2))
               
fave_word_3 = 'catz'
# add 'world' and a random number (between 0-3) of 'Bob's to this word
print(add_bob (fave_word_3))

