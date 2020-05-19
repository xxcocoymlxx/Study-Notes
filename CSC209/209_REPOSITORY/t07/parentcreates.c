#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main(int argc, char **argv) {

	int i;
	int n;
	int num_kids;

	if (argc != 2) {
		fprintf(stderr, "Usage: parentcreates <numkids>\n");
		exit(1);
	}

	num_kids = strtol(argv[1], NULL, 10);
	pid_t ppid = getpid();

	for (i = 0; i < num_kids; i++) {
		if (getpid() == ppid){
			n = fork();
			if (n < 0) {
				perror("fork");
				exit(1);
			}
 			printf("pid = %d, ppid = %d, i = %d\n", getpid(), getppid(), i);
		}
	}
	if(ppid == getpid()){
		pid_t c_pid = 1;
		while ((c_pid = wait(NULL)) != -1){
		}
	}

	return 0;
}
