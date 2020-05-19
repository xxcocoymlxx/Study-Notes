#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int truncate(char *str, int num);
/*
    Write a function named truncate() that takes a string s and a
    non-negative integer n. If s has more than n characters (not including the
    null terminator), the function should truncate s at n characters and
    return the number of characters that were removed. If s has n or
    fewer characters, s is unchanged and the function returns 0. For example,
    if s is the string "function" and n is 3, then truncate() changes s to
    the string "fun" and returns 5.
*/

int main(int argc, char **argv) {
    /* Do not change the main function */
    if (argc != 3) {
        fprintf(stderr, "Usage: truncate number string\n");
        exit(1);
    }
    int amt = strtol(argv[1], NULL, 10);
    //note: command line argumant的顺序是先数字，再string！
    char *target = argv[2];

    int soln_val = truncate(target, amt);
    printf("%d %s\n", soln_val, target);

    return 0;
}

//to truncate a string, just put a '\n' after the index you want to truncate
//note: It's '\0', not "\0", it would cause a warning
int truncate(char *str, int num){
    int length;
    if(num<=0){
        return 1;
    }else if (strlen(str)<=num){
        return 0;
    }else{ //strlen(str)>num
        length = strlen(str)-num;
        str[num] = '\0';
        return length;
    }

}