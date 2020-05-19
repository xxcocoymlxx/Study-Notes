#include <unistd.h>

#ifndef ERAT_H
#define ERAT_H

int filter(int m, int readfd, int writefd);

//make_stage() could be roughly 20-40

// fds is a pointer to an array of 2 ints, suitable for using with pipe()
pid_t make_stage(int m, int read_fd, int **fds);

#endif
