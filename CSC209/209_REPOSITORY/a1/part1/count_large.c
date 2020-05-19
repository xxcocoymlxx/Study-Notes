#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//now

// TODO: Implement a helper named check_permissions that matches the prototype below.
int check_permissions(char *, char *);

int main(int argc, char** argv) { 

	//这一行就是把bash command放里面他就可以运行command line
	//然后把ls的结果print到out.txt里
	//system("/bin/ls -l > out.txt");
	//这一行是把out.txt里的内容redirect作为standard input（原本stdin是keyboard）
    //freopen("out.txt","r",stdin);
    //然后我们就可以用scanf来筛选和抓取有用信息了
    //我们需要
	//system("/bin/ls -l | count_large");


	//醉了。。。pipe是在terminal里打的，redirect output并不是在这个file里完成的：）

    //我们从file里读取出信息，读完了一定要预留位子给终止符！
	char required_permission[15], file_permission[15];
	int required_size, file_size;
	int count = 0;


	// TODO: Process command line arguments.

	// argc比我真实的argument多1，不给argument也是1
	//第二个argv是一个我们给的argument的array的double pointer
	//这里array里的0号位是他的默认值，1号位开始才是我们的第一个argument
    if (!(argc == 2 || argc == 3)) { //如果我们给的argument的数量不是1或2，就error
        fprintf(stderr, "USAGE:\n\tcount_large size [permissions]\n");
        return 1;//return 0表正确，return 1表示function有问题
    }else if (argc == 2){ //only 1 argument, the file size as a STRING! have to convert it to a integer
    	required_size= strtol(argv[1],NULL,10); //this doesn't need the strcpy(), its not a STRING
    	strncpy(required_permission,"---------",sizeof(required_permission));//NEVER use strcpy()!
    } else if (argc == 3){ //2 arguments, the file size & file permission (str of 9 char)
    	required_size = strtol(argv[1],NULL,10);
    	strncpy(required_permission ,argv[2],sizeof(required_permission));
    }

    // TODO: Call check_permissions() and then print the returned value.

    // read the first line : total number of lines
    scanf("%*s %*d");

    //only 【file permission】 and 【file size】 are gonna be read and assigned, other values are read but not assigned
    //scanf from the stdin, aka the out.txt
    //note: 这里一定要写EOF，因为如果没有的话会出现infinite loop，会循环读取out.txt里的内容
    //Directories are not considered to be regular files!!
    while(scanf("%s %*d %*s %*s %d %*s %*s %*s %*s", file_permission, &file_size) != EOF){
    	//printf("%s %d\n",file_permission,file_size);
    	//&&(file_permission[0]!='d')
    	//printf("%c\n",file_permission[0]);
    	if((file_size > required_size)&&(file_permission[0]!='d')&&(check_permissions(file_permission, required_permission) == 0)){
    		count++;
    		//printf("%s %d\n",file_permission,file_size);
    	}
    }

    printf("%d\n", count);
    return 0;
	}

//The function will return 0 if the file has all 
//the required permissions and 1 otherwise. 
int check_permissions(char *file_permission, char *required_permission){
	int i;
	//create a new char* and point it to the 2nd character of your array
	//printf("%c\n",file_permission[0]);
	char *permission = file_permission+1;
	//printf("%s\n",permission);

	//用loop把9个element的file permission一个一个elm的检查
	//note：“-” is always less than “r”“w”“x”
	for (i = 0; i < strlen(file_permission); ++i)
	{
		if (permission[i] < required_permission[i])
		{
			return 1;
		}
	}
	return 0;

}
