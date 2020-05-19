#include <stdio.h>

int main(){
	int num;
	char phone_number[10];

	while(scanf("%s %d", phone_number, &num) != EOF){ //to quit with control+d

		if (num == 0){
        		printf("%s", phone_number);
        		printf("\n");
	
       		 } else if ((num >= 1) && (num <= 9)){

             		printf("%c", phone_number[num]);
             		printf("\n");
       		 }
	}
	
	return 0;
}
