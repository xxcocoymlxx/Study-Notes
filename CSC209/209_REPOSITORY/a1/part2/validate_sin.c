#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int populate_array(int, int *);
int check_sin(int *);


int main(int argc, char **argv) {
    // TODO: Verify that command line arguments are valid.
    int SIN_array[9];
	int sin_number;

	//user calls the program with too few or too many arguments, 
	//the program should return 1
	if (argc != 2) {
        return 1;
    }

    // TODO: Parse arguments and then call the two helpers in sin_helpers.c
    // to verify the SIN given as a command line argument.
	sin_number = strtol(argv[1],NULL,10);

	if (populate_array(sin_number, SIN_array) == 1){ //not 9 digit number
		printf("Invalid SIN\n");
	} else if ((populate_array(sin_number, SIN_array) == 0)&&(check_sin(SIN_array) == 0)){ //a 9 digit number
		printf("Valid SIN\n");
	} else {
		printf("Invalid SIN\n");
	}
  
    return 0;
}
