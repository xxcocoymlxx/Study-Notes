#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "helpers.h"

#define RAND_RANGE 4

/* NOTE: This program does nothing useful. It just reads from STDIN, emits
 * to STDOUT, and occasionally reports that it fails ...
 */
int main() {
    int retval = read_data();

    srand(time(NULL));
    if (retval < 0 || rand() % RAND_RANGE == 0) {
        printf("Failed\n");
        return 1;
    }
    return 0;
}
