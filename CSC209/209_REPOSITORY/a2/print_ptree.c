#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>//to use isdigit()
#include <string.h>

#include "ptree.h"

//If there is some sort of error that is not a command line error, return 2

int main(int argc, char **argv) {
    // TODO: Update error checking and add support for the optional -d flag
    // printf("Usage:\n\tptree [-d N] PID\n");
    if (argc!=2 && argc!=4){ //check number of arguments
    	fprintf(stderr, "Insufficient or too many arguments are provided.\n");
    	return 1;
    }

    //If a PID or EXE is not found, continue building the tree, 
    //return 1 in generate_ptree, and then print what you can in print_ptree. 
    //Then return 2 in main.
    if ((argc==4) && (strncmp(argv[1],"-d",strlen(argv[1]))==0) && (isdigit(*argv[2])!=0) && (isdigit(*argv[3])!= 0)){
    	struct TreeNode *root = NULL;
    	if (generate_ptree(&root, strtol(argv[3], NULL, 10))==1){ //这时root已经是一整个tree了
            print_ptree(root, strtol(argv[2], NULL, 10));
            //printf("return value of generate_ptree is 1\n");
    		return 2;
    	}
        print_ptree(root, strtol(argv[2], NULL, 10));
        //printf("return value of generate_ptree is 0\n");
    	

    }else if ((argc==2) && (isdigit(*argv[1])!=0)){
    	// NOTE: This only works if no -d option is provided and does not
    	// error check the provided argument or generate_ptree. Fix this!
    	struct TreeNode *root = NULL;
    	if (generate_ptree(&root, strtol(argv[1], NULL, 10)) == 1){ //这时root已经是一整个tree了
            print_ptree(root, 0);//print这个tree
            //printf("return value of generate_ptree is 1\n");
    		return 2;
    	}
    	print_ptree(root, 0);
        //printf("return value of generate_ptree is 0\n");

    }else{
        fprintf(stderr, "incorrect command line argumant usage\n");
    	return 1;
    }
}

