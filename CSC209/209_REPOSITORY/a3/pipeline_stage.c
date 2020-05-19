#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include "eratosthenes.h"


//acts like a passthrough between main and filter.


// read end, fildes[0] 
//write end, fildes[1]

//the parameter int n is actually filter value m
pid_t make_stage(int n, int read_fd, int **fds) {
    // TODO: Complete
    int *actual_fds = *fds;//to avoid unnecessary double-pointer confusion

    if (pipe(actual_fds)==-1) exit(255);

    int r = fork();
    if (r < 0) exit(255);
	else if (r > 0){//parent process
    	//filter会把筛选完的数字直接写到child process里的
    	//no need to read from the child
    	if (close(actual_fds[0])==-1) exit(255);

    	//把从main里读来的num list再传到filter里去读
    	if (filter(n,read_fd,actual_fds[1])!=0) exit(255);

    	if (close(actual_fds[1])==-1) exit(255);

    	if (close(read_fd)==-1) exit(255);
    	return r;//The parent process returns the child's PID
    	
    }else{//child process, it will use actual_fds pipe for the next level
    	//只要是child process就return，然后就回到main里面继续筛选
    	if (close(actual_fds[1])==-1) exit(255);
        if (close(read_fd)==-1) exit(255);//这个要关，因为fork了以后也是完全复制的，child process里也有这个开着的read_fd
    	return r;
    }
}
