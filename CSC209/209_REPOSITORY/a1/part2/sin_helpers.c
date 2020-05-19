#include <stdio.h>

// TODO: Implement populate_array
/*
 * Convert a 9 digit int to a 9 element int array.
 */
int populate_array(int sin, int *sin_array) {
	//I think this is the meaning of "only consider numbers that begin 
	//with a non-zero digit to be valid""
	if (!((sin > 99999999) && (sin <= 999999999))){ //NOT 9 digits
		return 1;
	}

	int i = 8;
	while (i >= 0){
		sin_array[i] = sin%10;
		sin = sin/10;//int除int只能整除，没有float division，比如10/3=3
		i--;
	}
    return 0;
}

// TODO: Implement check_sin
/* 
 * Return 0 (true) iff the given sin_array is a valid SIN.
 */
int check_sin(int *sin_array) {
    int total = 0;
    int i;
	for (i = 0; i < 9; i++){//sin number双数index乘1，单数index乘2
		if (i%2==0){
			total += sin_array[i];
		} else {
			if ((sin_array[i]*2) >= 10){
				total += (sin_array[i]*2)/10;
				total += (sin_array[i]*2)%10;
				}else{
					total += sin_array[i]*2;
				}
			}
		}//for loop end

		if(total%10 == 0){
			return 0;
		} else {
			return 1;
		}
	}//function ends
