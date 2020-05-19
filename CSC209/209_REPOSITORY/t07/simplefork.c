#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
	int ret;

	printf("A\n");
	ret = fork();//返回的是child PID， or -1

	printf("B\n");
	if(ret < 0) {
		perror("fork");
		exit(1);

	} else if (ret == 0) {
		printf("C\n");

	} else {
		printf("D\n");
	}

	printf("E\n");
	return 0;
}
