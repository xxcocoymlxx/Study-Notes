#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <time.h>


#ifndef MESSAGE
    #define MESSAGE "Peter Piper and Peppers\r\n"
#endif


int main(int argc, char **argv) {
    printf(MESSAGE);

    if (argc == 2) {
        printf("Argument: %s\r\n", argv[1]);
    }

    return 0;
}
