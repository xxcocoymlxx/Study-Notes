#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <time.h>


#ifndef MESSAGE
    #define MESSAGE "Peter Piper and Peppers\r\n"
#endif


int main(int argc, char **argv) {
    sleep(5);

    printf(MESSAGE);

    return 0;
}
