#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <time.h>


#ifndef MESSAGE
    #define MESSAGE "A stitch in time\r\n"
#endif
#ifndef MINCHARS
    #define MINCHARS 3
#endif
#ifndef MAXCHARS
    #define MAXCHARS 7
#endif
#ifndef MAXDELAY
    #define MAXDELAY 200000000
#endif


// Defining function to write a message in pieces with a delay
void write_random_pieces(const char *message, int times);


int main(int argc, char **argv) {
    char *endptr = NULL;
    int num_times;
    if (argc != 2 || (num_times = strtol(argv[1], &endptr, 10)) == 0
                  || *endptr != '\0') {
        fprintf(stderr, "Usage: randprint num_times\n");
        exit(1);
    }

    srandom(0);       // Not seeding with time, so that behaviour is deterministic
    write_random_pieces(MESSAGE, num_times);

    return 0;
}


/*
 * Write the given message the given number of times to STDOUT in randomly-sized
 * pieces with pauses. Does NOT write any null-terminator characters.
 */
void write_random_pieces(const char *message, int times) {
    char piece[MAXCHARS];
    int message_len = strlen(message);
    int total_bytes = times * message_len;
    int current_byte = 0;

    while (current_byte < total_bytes) {
        int piece_size = rand() % (MAXCHARS - MINCHARS + 1) + MINCHARS;
        int bytes_left = total_bytes - current_byte;
        if (piece_size > bytes_left) {
            piece_size = bytes_left;
        }

        for (int i = 0; i < piece_size; i++) {
            piece[i] = message[(current_byte + i) % message_len];
        }
        if (write(STDOUT_FILENO, piece, piece_size) != piece_size) {
            perror("write");
            exit(1);
        }
        current_byte += piece_size;

        struct timespec sleeptime = { .tv_sec = 0, .tv_nsec = random() % MAXDELAY + 1};
        nanosleep(&sleeptime, NULL);   // Ignoring error -- we just returned early
    }
}
