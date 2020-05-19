#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <signal.h>
#include <sys/time.h>


int main(int argc, char const *argv[]){
	if (argc != 2){
		fprintf(stderr, "wrong number\n");
		exit(1);
	}

	int curr;
	FILE *fd = fopen(argv[1],"wb");

	srandom(time(NULL));
	for(int i = 0; i < 100; i++){
		curr = (int)random()%100;
		fwrite(&curr, sizeof(int),1,fd);
	}
	fclose(fd);

	return 0;
}