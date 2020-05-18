class MyError(Exception):
    pass

try:
    #code

    l = []

    #l[2]
    
    #1/0

    a = 2
    
    assert a==0, 'a is not 2'

    if a < 3:
        raise MyError('eeeeee')

    elif a > 8:
        raise NameError
    
    print('done')

    

except MyError:
    print('my error')
    
except IndexError as a:
    print('1111',a)

except AssertionError as e:
    print(100000,e)
    
except NameError:
    print(22222)


##except Exception:
##    print('aaaa')


else:
    print('no error')

finally:
    print('always do')
    
print('..........')
