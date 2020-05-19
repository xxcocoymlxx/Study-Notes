#include <stdio.h>
#include <stdlib.h>
#include "eratosthenes.h"

// filter() can be done in about 10 lines of code
//the parameter int n is actually filter value m
int filter(int n, int readfd, int writefd) {
    // TODO: Complete

    int num;
    int result;
    while (1){
        if ((result = read(readfd,&num,sizeof(int))) > 0){
    	   if(num%n != 0){
    		  if (write(writefd, &num, sizeof(int)) == -1) return 1;
            }
        }
        else if (result == -1) return 1;
        else if (result == 0) return 0;
    }
}

