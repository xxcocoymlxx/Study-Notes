#include <stdio.h>
#include <string.h>
//#incldue <stdlib.h>

#define MAXS 20

int main(){
	char first[MAXS] = "Monday"; //less of change of buffer overflow
	//a char array in stack

	char *second = "Tuesday"; //a string literal on stack
	//second这个variable是在stack里，指向存在program data里的一个value

	char *third = malloc(sizeof(char)*MAXS); //on heap,
	//third这个variable是存在stack里的，指向存在heap里的一个value

	//third = "wuifwgrew";
	//这相当于把这个存在program data里的string的address放进third这个variable里，就会出现memory leak

	strncpy(third,"Wednesday",MAXS-1);

	CHAR *_first =first;
	char **string_list[] = {&_first,&second,&third};
	//一个char**是char*的一个pointer，有char*的address
	//first和second都是char*，所以char**可以直接指向他们
	//first is not a char*,but name of a array can be used as an pointer
	//所以char **不能等于&first, there's no memory that stores the address of first,
	//所以我们只能建一个CHAR *_first =first;我们现在就有first的address了， pointes to first
	//所以现在char **string_list[]里就有3个address了，each points to a value

	char *string_list2[] = {first,second,third};
	//一个array of char *，
	//first就指向了char first[MAXS]这个array
	//second，copy了second这个char*的值放在了
	//我们就有两个char* pointing to the same value, sacond在这里也就直接指向program data里的那个值
	//which is read only，我们不能改变他，所以我们重新建一个可改变的value然后让second这个pointer指向他，所以才会有我们之后print出来的“Tue”
	//third,也是一个char*,

	third[3] = '\0';
	first[3] = '\0';

	//second = "Tue";
	second = malloc(sizeof(char)*MAXS);
	strncpy(second,"Tue",MAXS-1);

	//如果加了下面这一行code，就两个prinf statement都会print出“montue wed”
	//string_list[1] = second;

	printf("%s\n%s\n%s",*string_list[0],*string_list[1],*string_list[2])
	//you have to dereference them
	//this is gonna print "Mon Tue Wed"
 	printf("%s\n%s\n%s",string_list2[0],string_list2[1],string_list2[2])
 	//first are pointing to the strings themselves 
 	//其他两个直接指向存在其他memory的value（而不是指向在stack上的variable）
 	////this is gonna print "Mon Tuesday Wed"


	//or 可以做一下的方法
	//third[0] = 'W';
	//third[1] = 'e';//note: single quote only for chars

	//note:
	//*third = "Wednesday";//就错了，这相当于把array的第一个elm变成了wednesday，因为
	//这是一个array第一个elm的pointer
	return 0;
}