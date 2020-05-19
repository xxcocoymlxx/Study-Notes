#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>

int main(int argc, char **argv) {

	int i;
	int n;
	int num_kids;

	if (argc != 2) {
		fprintf(stderr, "Usage: childcreates <numkids>\n");
		exit(1);
	}

	num_kids = strtol(argv[1], NULL, 10);
	pid_t ppid = getppid();//加的,要include types.h
	pid_t child_pid;
	int status;


	for (i = 0; i < num_kids; i++) {
		if (ppid != getpid()){//第一次为空，因为第一次没有parent //加的
			ppid = getpid(); //加的
			n = fork();
			if (n < 0) {
				perror("fork");
				exit(1);
			}//他在空跑，空跑比fork快，比fork快结束，父程序结束了，那下面的孩子程序的主程序就是主程序了
			//父程序的比子程序先结束了，所以print ppid的时候显示的都是1

/*
	//第二种：关掉了parent程序，那孩子的parent就是系统主程序了，系统主程序的ppid就是1
	//num_kids = strtol(argv[1], NULL, 10);

	for (i = 0; i < num_kids; i++) {
			n = fork();
			if (n < 0) {
				perror("fork");
				exit(1);
			}
			printf("pid = %d, ppid = %d, i = %d\n", getpid(), getppid(), i);
			if (n>0){
				exit(0);
			}
*/

		if (n == 0){ //只打印父亲，孩子不打印
 			printf("pid = %d, ppid = %d, i = %d\n", getpid(), getppid(), i);
 			}
	}
}

	//wait(NULL);
	child_pid = wait(&status);//19本身没有任何子程序，他的返回值是-1
	/*
	if (WIFEITED(status)){
		printf("child process[%d] exited with %d\n", child_pid, WEXITSTATUS(status));
	}
	*/
	return 0;
}
