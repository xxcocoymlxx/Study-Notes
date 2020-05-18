SIGN_GROUPS = '[ARI,LEO,SAG],[TAU,VIR,CAP],[GEM,LIB,AQU],[PIS,SCO,CAN]'

SIGNS = 'ARI:03,21-04,19;TAU:04,20-05,20;GEM:05,21-06,21;CAN:06,22-07,22;' + \
        'LEO:07,23-08,22;VIR:08,23-09,22;LIB:09,23-10,23;SCO:10,24-11,20;' + \
        'SAG:11,21-12,21;CAP:12,22-01,20;AQU:01,21-02,21;PIS:02,22-03,20;'

def get_sign_group(sign):
    '''
    >>> get_sign_group('ARI')
    0

    >>> get_sign_group('CAN')
    3
    '''
    i = 0
    group_number = 0
    while i < len(SIGN_GROUPS):
        if SIGN_GROUPS[i] != ']':
            i += 1
        elif SIGN_GROUPS[i] == ']':
            group = SIGN_GROUPS[i-12:i+1]
            #print(group)
            i += 1
            if sign not in group:
                group_number += 1
            else:
                return group_number

            
def find_astrological_sign(month, date):
    '''
    >>> find_astrological_sign(9, 2)
    'VIR'
    
    >>> find_astrological_sign(10, 23)
    'LIB'

    '''
    i = 0
    while i + 16 <= len(SIGNS):
        if (int(SIGNS[i+4:i+6]) == month and date >= int(SIGNS[i+7:i+9])) or \
           (int(SIGNS[i+10:i+12]) == month and date <= int(SIGNS[i+13:i+15])):
            return SIGNS[i:i+3]
            
        else:
            i = i + 16
