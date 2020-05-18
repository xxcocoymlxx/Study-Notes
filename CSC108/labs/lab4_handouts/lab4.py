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



def decode_phrase(phrase):
    '''(str) -> str

    Given a multi-character string 'phrase', return the whole phrase
    decoded.
    
    Only alphabetical characters should be changed. All other
    characters (e.g. special characters or whitespace) should
    stay the same.

    # Add in examples

    '''
    for item in phrase:
        decoded
        if ord(item) >= 97 and ord(item) <= 122:
            val = ord(item) + 2

 

if __name__ == "__main__":
    
    print("The mystery message decoded is:")
    print(decode_phrase("g fmnc wms bgblr rpylqjyrc gr zw fylb. " \
                        "rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw " \
                        "fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq "\
                        "qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. "\
                        "lmu ynnjw ml rfc spj."))

    
