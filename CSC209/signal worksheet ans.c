#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
//task 1
int main(){
	while (1){
		pause();
	}
	return 0;
}

//task 4
void sing(int n){
	printf("Happy birthday to you\n");
	printf("Happy birthday to you\n");
	printf("Happy birthday dear BOB\n");
	printf("Happy birthday to you\n");

}

int main(){
	struct signaction newact;
	newact.sa_handler = sing;
	newact.sa_flags = 0;
	sigemptyset(&newact.sa_mask);

	if (signaction(SIGUSER1, &newact, NULL) == -1){
		perror("sigaction");
		exit(1);
	}
	while (1){
		pause();
	}
	return 0;
}
//在terminal里, 每次send一个signal，就print birthday song
//kill -SIGUSER1 PID

//tack 7
static char *name = NULL;
void sing(int n){
	printf("Happy birthday to you\n");
	printf("Happy birthday to you\n");
	printf("Happy birthday dear %s\n", name);//把这里的名字改成user input的名字
	printf("Happy birthday to you\n");

}

int main(int argc, char **argv){
	//error checking for comman line argument
	name = argv[1];

	struct signaction newact;
	newact.sa_handler = sing;
	newact.sa_flags = 0;
	sigemptyset(&newact.sa_mask);

	if (signaction(SIGUSER1, &newact, NULL) == -1){
		perror("sigaction");
		exit(1);
	}
	while (1){
		pause();
	}
	return 0;


//task 8
//result：无论你call几次signal，都只会print出两次，他在blocking SIGNALS of the same type
//第四第五次值会keep one copy, the first finishes, will unblock the next
//
static char *name = NULL;
void sing(int n){
	printf("Happy birthday to you\n");
	printf("Happy birthday to you\n");
	sleep(5);
	printf("Happy birthday dear %s\n", name);//把这里的名字改成user input的名字
	printf("Happy birthday to you\n");

}

int main(int argc, char **argv){
	//error checking for comman line argument
	name = argv[1];

	struct signaction newact;
	newact.sa_handler = sing;
	newact.sa_flags = 0;
	sigemptyset(&newact.sa_mask);

	if (signaction(SIGUSER1, &newact, NULL) == -1){
		perror("sigaction");
		exit(1);
	}
	while (1){
		pause();
	}
	return 0;


//another example
static char *name = NULL;
void sing(int n){
	printf("Happy birthday to you\n");
	printf("Happy birthday to you\n");
	sleep(5);
	printf("Happy birthday dear %s\n", name);//把这里的名字改成user input的名字
	printf("Happy birthday to you\n");

}

int main(int argc, char **argv){
	//error checking for comman line argument
	name = argv[1];

	struct signaction newact;
	newact.sa_handler = sing;
	newact.sa_flags = sa_nodiffer;//it's interupting itself
	sigemptyset(&newact.sa_mask);

	if (signaction(SIGUSER1, &newact, NULL) == -1){
		perror("sigaction");
		exit(1);
	}
	while (1){
		pause();
	}
	return 0;

//task 9
//send a signal and call SIGINT, the program will be terminated
//now we dont want it to be terminated, want to block sigint

//not modified YET
static char *name = NULL;
void sing(int n){
	printf("Happy birthday to you\n");
	printf("Happy birthday to you\n");
	sleep(5);
	printf("Happy birthday dear %s\n", name);//把这里的名字改成user input的名字
	printf("Happy birthday to you\n");

}

int main(int argc, char **argv){
	//error checking for comman line argument
	name = argv[1];

	struct signaction newact;
	newact.sa_handler = sing;
	newact.sa_flags = sa_nodiffer;//it's interupting itself
	sigemptyset(&newact.sa_mask);

	if (signaction(SIGUSER1, &newact, NULL) == -1){
		perror("sigaction");
		exit(1);
	}
	while (1){
		pause();
	}
	return 0;

//task 10
static char *name = NULL;
void sing(int n){
	printf("Happy birthday to you\n");
	printf("Happy birthday to you\n");
	sleep(5);
	printf("Happy birthday dear %s\n", name);//把这里的名字改成user input的名字
	printf("Happy birthday to you\n");

}

int main(int argc, char **argv){
	//error checking for comman line argument
	name = argv[1];

	struct signaction newact;
	newact.sa_handler = sing;
	newact.sa_flags = sa_nodiffer;//it's interupting itself
	sigemptyset(&newact.sa_mask);

	if (signaction(SIGUSER1, &newact, NULL) == -1){
		perror("sigaction");
		exit(1);
	}
	while (1){
		pause();
		if (sing_song)
	}
	return 0;





