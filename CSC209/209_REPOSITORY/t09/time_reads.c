#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <signal.h>
#include <sys/time.h>


// Message to print in the signal handling function. 
#define MESSAGE "%ld reads were done in %ld seconds.\n"


/* Global variables to store number of read operations and seconds elapsed.
 * These have to be global so that signal handler to be written will have
 * access.
 */
long num_reads = 0, seconds;


void handler (int signo) {
    fprintf(stderr, MESSAGE, num_reads, seconds);
}


int main(int argc, char ** argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: time_reads s filename\n");
        exit(1);
    }
    seconds = strtol(argv[1], NULL, 10);

    FILE *fp;
    if ((fp = fopen(argv[2], "rb")) == NULL) {    // Read+Write for later ...
      perror("fopen");
      exit(1);
    }

    /* In an infinite loop, read an int from a random location in the file
     * and print it to stderr.
     */

    struct sigaction newact ;
    sigemptyset(&newact.sa_mask ); 
    newact.sa_flags = 0;
    newact.sa_handler = handler ;
    if (sigaction(SIGPROF, &newact, NULL) == -1)
    exit(1);

    struct itimerval itimer;
    itimer.it_value.tv_sec = seconds;
    itimer.it_value.tv_usec = 0;

    itimer.it_interval.tv_sec = seconds;
    itimer.it_interval.tv_usec = 0;

    setitimer(ITIMER_PROF, &itimer, NULL);


    int curr;
    int index;
    srandom(time(NULL));
    
    for (;;) {
      index = (int)random()%100;
      for (int i = 0; i <= index; ++i)
      {
        fread(&curr,sizeof(int),1,fp);
      }
      fprintf(stderr, "%d\n", curr);
      fseek(fp,0,SEEK_SET);
      num_reads++;

    }

    fclose(fp);

    return 1;  //something is wrong if we ever get here!
}

