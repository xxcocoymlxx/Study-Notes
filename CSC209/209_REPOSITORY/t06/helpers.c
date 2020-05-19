#include <stdio.h>

#include "helpers.h"

int read_data() {
    char buffer[BUF_SIZE];
    int retval;

    while ((retval = fread(buffer, 1, BUF_SIZE, stdin)) == BUF_SIZE);

    return retval;
}
