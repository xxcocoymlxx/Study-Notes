#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>//to use isdigit()
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <math.h>
#include <sys/types.h>
#include <unistd.h>

#include "eratosthenes.h"

// read end, fildes[0] 
//write end, fildes[1]

int main(int argc, char *argv[]) {
    // Turning off sigpipe
    if (signal(SIGPIPE, SIG_IGN) == SIG_ERR) {
        perror("signal");
        exit(1);
    }

    //(remaining != NULL)
    //if command line argument is incorrect format
    if ((argc != 2) || (isdigit(*argv[1])==0) || (strchr(argv[1], '.') != NULL)){
    	fprintf(stderr, "Usage:\n\tpfact n\n");
    	exit(1);
    }

    for (int i= 0; i < strlen(argv[1]); i++){
    	if (isdigit(argv[1][i]) == 0){
    		fprintf(stderr, "Usage:\n\tpfact n\n");
    		exit(1);
    	}
    }
    //char *remaining = NULL;
    int n = strtol(argv[1], NULL, 10);

    if ((n <= 1)){
    	fprintf(stderr, "Usage:\n\tpfact n\n");
    	exit(1);
    }

    // Your solution below ...
    int fd[2];
    if(pipe(fd) == -1) exit(2);

  	pid_t r = fork();
   	if(r == -1) exit(2);

  	else if (r == 0){//the child process
      static int loop_counter = 0;
      //the filter is not gonna exceeds 255, so no more than 255 potential prime factors
      int factors[255];//create an array to store all the potential prime factors
      int num_factors = 0;//number of factors currently found
      int current_readfd = fd[0];//we are gonna use this to loop, the actual reading fd is different in every iteration
 
      //close the write end of the pipe
      if (close(fd[1])==-1) exit(255);

      int num = 0;//the next numbers we are reading from the pipe
      int m = 0;//the first number must be m, then update this value later
      int next_PID = 0;// the PID retuned from make_stage()
      int bytes_read = 0;//bytes the child process read from the pipe, if it equals 0 then it has nothing more to read


      //一个超级大的while，只要make_stage还在往下做，就一直循环while
      while (next_PID == 0){

        //if number of filters exceeds 255, we dont event print anything, just exit
        if (loop_counter >= 255) exit(255);

        if ((bytes_read = read(current_readfd, &num, sizeof(int))) < 0){// bytes_read < 0, error occured
          if (close(current_readfd)==-1) exit(255);
          exit(255);
        }
        //每次从current_readfd里读出来的东西肯定是下一个m的
        else if (bytes_read > 0){//先读出一个2

         //we only store the primes that are potential factors
         //我们只存factors
         if (n%num == 0){
         factors[num_factors] = num;
         num_factors++;
         }
         m = num;//刷新新的m

         //一直在现有的potential factors array里寻找我们要的factors，一旦遇到了，就得出结果
         //也就是要在call下一个filter前先check我们是否已经找到了我们要的factors

         if (num_factors >= 2) {
            printf("%d is not the product of two primes\n", n);
            if (close(current_readfd)==-1) exit(255);
            exit(0);
          }
         
         for (int i = 0; i < num_factors; i++){

            if (n%(factors[i]*num)== 0){
             if (factors[i]*num == n) printf("%d %d %d\n", n, factors[i], n/factors[i]);
             else printf("%d is not the product of two primes\n", n);
             if (close(current_readfd)==-1) exit(255);
             exit(0);
            }
          }
        
        //出了inner while loop，已经读不出来东西了，进入到最下面一层的process了
        //就说明我们的所有prime potential factors都已经找到了
        //现在就要判断我们是否能在所有primes里面找到factors了
        } else if (bytes_read == 0){
          
         for (int i = 0; i < num_factors; i++){
            if (n%factors[i] == 0){
              printf("%d %d %d\n", n, factors[i], n/factors[i]);
              if (close(current_readfd)==-1) exit(255);
              exit(0);
            }
         }

         //如果这个for loop结束以后还没有找到factor，那他就是个prime了
          if (num_factors == 0) {
            printf("%d is prime\n", n);
            if (close(current_readfd)==-1) exit(255);
            exit(0);
          }

        }

      //接下来我们要把2放进filter里（也就是call make_stage）筛掉不要的数字
      //然后把剩下的数字再往下传
      //call make_stage 必须在while的里面and最后，这是while loop继续run的条件，不能再任何一个if里
        int *fds; //事实证明这个pipe还是一定要malloc。。不然make_stage都call不了
        int newfd[2];
        fds = newfd;
        next_PID = make_stage(m,current_readfd,&fds);//make_stage(int n, int read_fd, int **fds)
        loop_counter++;
        current_readfd = newfd[0];//注意这里我们把fds放进去作为下一层pipe
        //并且也是filter写出来的pipe！

      }//big while loop ends

      //上面那个大while只是给make_stage里出来的child process走的
      //从make_stage里出来的parent process进不去上面那个while，会来这里等着他的child
      int status;
      if(waitpid(next_PID, &status, 0)!= -1){
        if(WIFEXITED(status)){
          if (WEXITSTATUS(status) >= 255) exit(255);
          }
          exit(WEXITSTATUS(status)+1);
        } 
    
  	}else{//the parent process

      //close the read end
      if (close(fd[0])==-1) exit(2);

      //write the integers from 2 to sqrt(n) to the pipe
      for(int i = 2; i <= sqrt(n); i++){
          if(write(fd[1], &i, sizeof(int)) == -1 ){//一直往child process写
            //如果没写成功的话
            //close the write end of pipe and break the loop
            //cause a broken pipe
            if (close(fd[1])==-1) exit(2);
            i = n;//make the loop guard invalid
          }     
      } 
      //写完了就把writing end关掉
      if (close(fd[1])==-1) exit(2);

      //get the exit status of its children process and print it
      //在这里收集他所有的child的exit code
      int status;
      if(waitpid(r, &status, 0)!= -1){
        if(WIFEXITED(status)){
          if (WEXITSTATUS(status) >= 255) exit(2);//超过255个filters要exit    
          printf("Number of filters = %d\n", WEXITSTATUS(status));
          exit(0);//成功结束
        }
      }
      
    	}//the big else of the child process ends
  	}
