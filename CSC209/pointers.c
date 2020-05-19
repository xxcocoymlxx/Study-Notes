#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXS 20

int main(){
	char first[MAXS] = "Monday"; //less of chance of buffer overflow
	char *second = "Tuesday"; //a string literal on stack
	char *third = malloc(sizeof(char)*MAXS);
	strncpy(third,"Wednesday",MAXS-1); 
	third[10] = '\0';

	first[3] = '\0';
	third[3] = '\0';
	//second[3]= '\0';//Bus error: 10

	//second is pointing to the string literal. 
	//which is read only, so we can’t copy the new value to it.
	//we can allocate a new space for it and then copy
	//strncpy(second, "Tue",3);//Bus error: 10

	//第一种OK的做法
	second = "Tue";

	//第二种OK的做法
	second = malloc(sizeof(int)*MAXS);
	strncpy(second,"Tue",3);
	second[3] = '\0';

	//第一种:Mon Tue Wed
	//这个是把它变成了一个array of char *，所以里面每一个element都要求他是一个char *，所以我们要把first改变一下type
	char* _first = first;
	char **string_list[] = {&_first, &second, &third};
	printf("%s\n%s\n%s\n",*string_list[0],*string_list[1],*string_list[2]);


	//第二种:Mon Tue Wed
	char *string_list2[]= {first,second,third};
	printf("%s\n%s\n%s\n",string_list2[0],string_list2[1],string_list2[2]);
	
	return 0;
}