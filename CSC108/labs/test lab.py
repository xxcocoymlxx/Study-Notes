def decode_letter(letter):
    '''(str) -> str

    Given a 1-character string 'letter', return the letter decoded
    (shift the letter by two to the right).
    
    You may assume the given letter is lowercase.
    
    >>> decode_letter('m')
    'o'

    >>> decode_letter('g')
    'i'
    '''
    if letter == 'y' or 'z':
        val = ord(letter) -24
    else:
        val = ord(letter) + 2
    return chr(val)
