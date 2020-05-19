#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "ptree.h"
#include <sys/stat.h> //for lstat()
#include <ctype.h>// for isalpha()

#define FILENAME_LENGTH 64 //keep track of your string lengths
#define CHILDREN_LENGTH 1024

const unsigned int MAX_PATH_LENGTH = 1024;

// If TEST is defined (see the Makefile), will look in the tests 
// directory for PIDs, instead of /proc.
#ifdef TEST
    const char *PROC_ROOT = "tests";
#else
    const char *PROC_ROOT = "/proc";
#endif

//for creating paths to various files in order to view them and check if the file/directory exists
int check_filename(char *procfile, pid_t pid, const char *PROC_ROOT, char *directory){
	// Here's a trick to generate the name of a file to open. Note 
    // that it uses the PROC_ROOT variable
	struct stat st;
    if (strncmp(directory,"/children",9)==0){//这里第三个parameter不能是strlen（directory），因为”“的话是0，就会进入第一个if了
        if (snprintf(procfile, MAX_PATH_LENGTH + 1, "%s/%d/task/%d/children", PROC_ROOT, pid, pid) < 0) {
            fprintf(stderr, "snprintf failed to produce filename: %s\n", procfile);
            return 1;
        }
    }else{
    if (snprintf(procfile, MAX_PATH_LENGTH + 1, "%s/%d%s", PROC_ROOT, pid, directory) < 0) {
        fprintf(stderr, "snprintf failed to produce filename: %s\n", procfile);
        return 1;
    }
}

    //lstat() returns the status of a file
    if (lstat(procfile,&st)<0) return 1;
    return 0;

}

/*
 * Creates a PTree rooted at the process pid. The root of the tree is
 * placed in root. The function returns 0 if the tree was created 
 * successfully and 1 if the tree could not be created or if at least
 * one PID was encountered that could not be found or was not an 
 * executing process.
 * 这个function pass进来一个tree node的pointer的pointer，等这个function结束的时候（return 0）
 * 证明tree已经创建好了，此时的root就不是一个空tree了，而是连着一个完整的tree的root
 */
int generate_ptree(struct TreeNode **root, pid_t pid) { 
	char procfile[MAX_PATH_LENGTH + 1];
    int result = 0;
    int flag = 0;

 	//you shouldn’t create a Node if a proc/PID or proc/PID/exe do not exist
    //both proc/PID/cmdline and proc/PID/task/PID/children should exist, 
    //but they might be empty, in that case, set it to NULL
    //这里我们分别generate出了不同的path存到了procfile里，并check这个path存不存在
    //到第三个check_filename()的call时procfile就是cmdline的path了
    if ((check_filename(procfile,pid,PROC_ROOT,"")==1) || 
        (check_filename(procfile,pid,PROC_ROOT,"/exe")==1) ||
        (check_filename(procfile,pid,PROC_ROOT,"/cmdline")==1)) return 1;

    //pass进来的这个root是个空的，只是declare了，但没有assignment,会有error
    //我们现在才initialize了这个tree node

    //注意！！如果一个PID连上面那些if都过不去（不是valid PID或executing program）
    //就根本不创建node给他，所以这以这时这个function return 1，那pass进来那个root就是NULL
    //然后print_ptree那个function再判断如果root是NULL就直接return，不print
    *root = malloc(sizeof(struct TreeNode));
	if (*root == NULL) return 1;//if malloc fails
    (*root)->pid = pid;
    (*root)->child_procs = NULL;
    (*root)->next_sibling = NULL;
    //(我之前是在判断PID是否valid前就initialize了tree root，所以我print时才会出现segmentation fault)

    //首先要打开这个cmdline file我们才能读取这个文件
    //从cmdline里得到executable的名字
    FILE *f = fopen(procfile, "r");
    if (f == NULL) return 1;

    //因为struct里的name这个member是个pointer，所以malloc一个space让name pointer指向他
    char *filename = malloc(sizeof(char)*(FILENAME_LENGTH+1));
    if (filename == NULL) return 1;//if malloc fails

    char *temp = malloc(sizeof(char)*(FILENAME_LENGTH+1));
    if (temp == NULL) return 1;//if malloc fails

    char shorten_name[MAX_PATH_LENGTH + 1];


    char buf[MAX_PATH_LENGTH + 1];
    char *ptr;
    int j = 0;

    int char_read = fread(buf,sizeof(char),FILENAME_LENGTH,f);
    if (char_read == 0) (*root)->name=NULL; //找不到executable的name，set it to NULL
    else{//此时的buf已经是一整串string了，要把executable name提取出来
         //先读到第一个null terminator的地方
        //注意！就算我们把它放到一个char array里，第一个null terminator之后的东西也还是存在的！！！
        //只是你print或者用strlen看这个line的时候他只会算到第一个nullterminator之前！！但他还是在那里的！
        
         //check如果我们存下来的部分有'/'，就extract最后一个'/'后的内容
         //如果这个部分没有'/'，就只留下有character的部分

        buf[char_read] = '\0';//这一行非常重要！！不然后面就会有garbage value！！！


        //只截取出我们需要的最前面的一部分 /usr/bin/myprog\0args1\0args2
        //此时用strlen（）看buf的长度就只会算到第一个null terminator之前，所以只把null前面的内容复制给temp就好
        strncpy(shorten_name,buf,strlen(buf)+1);

        //searches string for the last occurrence of '/'
        temp = strrchr(shorten_name,'/');//temp就是最后一次"/"出现之后的string(包括'/')
        //returns a pointer to the last occurrence of character c in string or a null pointer if no matching character is found.


        if(temp == NULL){//executale string里没有’/‘
            //从后面往前找，loop结束后i就是最后一个是char的index，把后面不是char的东西都null terminate掉
            int i = strlen(shorten_name)-1;
            while ((i >=0) && (isalpha(shorten_name[i])== 0)){i--;}
            shorten_name[i+1] = '\0';

            //从前往后找，找到第一个不是alphabet的东西，让这个pointer移动到那个位置（除去了所有special character）
            ptr = shorten_name;
            i = 0;
            while(i<strlen(shorten_name) && (isalpha(shorten_name[i])== 0)){//is NOT a alphabet
                    j++;
                    i++;
                }
            ptr = ptr + j; 

            strncpy(filename,ptr,strlen(ptr)+1);//这个加1也非常重要！！包括了null terminator！
            (*root)->name = filename;//赋值当前tree node的name，有了这个name之后我们就可以去找他的children了
        }else{//executale string里有’/‘
            //此时filename里存的就是最后一次"/"出现之后的string
            (*root)->name = temp+1;//加1是要去掉'/'
        }
    }

    if (fclose(f) != 0) return 1;//if fclose() fails



    if (check_filename(procfile,pid,PROC_ROOT,"/task")==1) return 1;
    //我们要从task/PID/children里得到一串子文件的PID，要把他split开，分别用每个子PID来建TreeNode
    if (check_filename(procfile,pid,PROC_ROOT,"/children")==1) return 1;
    
    f = fopen(procfile,"r");
	if(f == NULL) return 1;

	char line[CHILDREN_LENGTH+1];//每次读一整行
	char_read = fread(line,sizeof(char),CHILDREN_LENGTH,f);//从fp里读取MAX_PATH_LENGTH个char放进buffer里
    if (char_read == 0) (*root)->child_procs = NULL;
    else{
        //to split the PIDs in the children file
	   char *token = NULL;
	   char *remaining = NULL;
	   token = strtok_r(line, " ", &remaining);

	   struct TreeNode *curr_child;
	   while (token){//得到了孩子的PID了，此时还是个string
	   //在这里建Tree Node
	   struct TreeNode *new_node = NULL;

       //the child_procs of root is a list that contains a pointer only to its first child
	   int pid = strtol(token, NULL, 10);
	  // if (generate_ptree(&new_node, pid)==0){//这一行一定不能要，不然child有错的话就根本不会继续build tree了
	      result = generate_ptree(&new_node, pid);

          //这他妈，这一行就花了我两个小时debugging，我之前的确是记录了generate_ptree的结果，然后return这个结果
          //但是！记住我们这是在一个while loop里面，我们每一个while loop只是tree的其中一个path
          //我记录了这一个path的return value，但是没把他“永远的记住”，等他到下一个loop iteration（下一个path）
          //result的值就会被刷新了！所以只要最后一个path的return value是0，最终就会return 0
          //但如果我们把它“永远的记住”，就是只要一旦有一个path的return value是1了，最终就return 1
          if (result == 1) flag = 1;

          //一定要有这一行，不然删除第二层孩子会有seg fault
          //就是说第二层如果错误的话，他后面的孩子和sibling就都不会print
          if (new_node != NULL){//这里还一定不能return！return的话while就结束了，他之后的所有children就都不会被print了
		      if ((*root)->child_procs == NULL){
			     (*root)->child_procs = new_node;
			     curr_child = new_node;
		      }else{
			     curr_child->next_sibling = new_node;
			     curr_child = new_node;
		      }
        }

	   token = strtok_r(NULL, " ", &remaining);//this is where the building continues
	   //if one child fails, the next child is gonna continue building.
		  }
        }
        if (fclose(f) != 0) return 1;//if fclose() fails
		return flag;
	}

/*
 * Prints the TreeNodes encountered on a preorder (先print root，再print左右) traversal of an PTree
 * to a specified maximum depth. If the maximum depth is 0, then the 
 * entire tree is printed.
 *
 * Each child process will be indented two spaces to 
 * the right with respect to its parent.
 *
 * Each line will contain the process's ID (its PID), 
 * a colon and a space, and the name of the executable.
 *
 * If the executable is not named, then the line will
 * just contain the PID (no colon, no space, no executable name).
 */
void print_ptree(struct TreeNode *root, int max_depth){
    // Here's a trick for remembering what depth (in the tree) you're at
    // and printing 2 * that many spaces at the beginning of the line.
    static int depth = 0;
    struct TreeNode *curr_child = NULL;

    if (root == NULL) return;

    //先print出depth*2的空格
    printf("%*s", depth * 2, "");

    //preorder (先print root，再print左右)
    if (root->name == NULL) printf("%d\n", root->pid);
    else printf("%d: %s\n", root->pid, root->name);

    if (max_depth == 1) return;

    depth++;
    curr_child = root->child_procs;

    while(curr_child!= NULL){
        print_ptree(curr_child, max_depth-1);
        curr_child = curr_child->next_sibling;
    }
    depth--;
}
