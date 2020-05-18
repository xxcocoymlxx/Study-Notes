import urllib.request

# Precondition for all functions in this module: Each line of the url
# file contains the average monthly temperatures for a year (separated
# by spaces) starting with January.  The file must also have 3 header
# lines.

def open_temperature_file(url):
    '''(str) -> file
    Open the specified URL, read past the three-line header, and 
    return the open file.
    '''

    pass


def avg_temp_march(f):
    '''(file) -> float
    Return the average temperature for the month of March
    over all years in f.
    '''

    # We are providing the code for this function
    # to illustrate one important difference between reading from a URL
    # and reading from a regular file. When reading from a URL,
    # we must first convert the line to a string.
    # the str(line, 'ascii') conversion is not used on regular files.
    
    march_temps = []

    # read each line of the file and store the values
    # as floats in a list
    for line in f:
        line = str(line, 'ascii') # now line is a string
        temps = line.split()
        # there are some blank lines at the end of the temperature data
        # If we try to access temps[2] on a blank line,
        # we would get an error because the list would have no elements.
        # So, check that it is not empty.
        if temps != []:
            march_temps.append(float(temps[2]))

    # calculate the average and return it
    return sum(march_temps) / len(march_temps)


def avg_temp(f, mo):
    '''(file, int) -> float
    Return the average temperature for month mo over all
    years in f. mo is an integer between 0 and 11, representing
    January to December, respectively.
    '''

    pass


def higher_avg_temp(url, mo1, mo2):
    '''(str, int, int) -> int
    Return either mo1 or mo2 (integers representing months in the
    range 0 to 11), whichever has the higher average temperature over
    all years in the webpage at the given URL.  If the months have the 
    same average temperature, then return -1.
    '''

    pass


def three_highest_temps(f):
    '''(file) -> list of float
    Return the three highest temperatures, in descending order, 
    over all months and years in f.
    '''

    pass


def below_freezing(f):
    '''(file) -> list of float
    Return, in ascending order, all temperatures below freezing 
    (32 degrees Fahrenheit), for all temperature
    data in f. Include any duplicates that occur.
    '''

    pass


url = 'http://robjhyndman.com/tsdldata/data/cryer2.dat'
