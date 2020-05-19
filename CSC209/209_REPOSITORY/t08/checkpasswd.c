#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAXLINE 256
#define MAX_PASSWORD 10

#define SUCCESS "Password verified\n"
#define INVALID "Invalid password\n"
#define NO_USER "No such user\n"

int main(void) {
  char user_id[MAXLINE];
  char password[MAXLINE];

  //read the user input for ./checkpasswd
  if(fgets(user_id, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }
  if(fgets(password, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }


  //creating the pipe
  int fd[2];
  if (pipe(fd) == -1){
      perror("pipe");
      exit(1);
  }

  //create a new process
  int r = fork();

  if (r > 0){//parent process

    if (close(fd[0])==-1){//will write to the child process
        perror("close pipe");
        exit(1);
    }

    //writing to pipe
    //note:can only write to the pipe "MAX_PASSWORD" bytes of chars, o.w. will error
    if (write(fd[1], user_id, MAX_PASSWORD) == -1) {
        perror("write to pipe");
        exit(1);
    }
    if (write(fd[1], password, MAX_PASSWORD) == -1) {
        perror("write to pipe");
        exit(1);
    }

    if (close(fd[1])==-1){//after using the pipe, you should also close the writing end
        perror("close pipe");
        exit(1);
    }

    //checking the exit status of the child
    int status;
    if (wait(&status) != -1)  {
        if (WIFEXITED(status)) {
          if (WEXITSTATUS(status)==0){
            printf("%s",SUCCESS);
          }else if (WEXITSTATUS(status)==2){
            printf("%s",INVALID);
          }else{
            printf("%s",NO_USER);
          }
        }
      }

  }else if (r == 0){//child process
    //child reads from pipe and writes to parent

    if (close(fd[1])==-1){//will receive input from the parent process
        perror("close pipe");
        exit(1);
      }

    //redirecting the input from the pipe to the stdin
    //so ./validate can receive the input from the stdin
    if (dup2(fd[0],fileno(stdin))==-1){
        perror("dup2");
        exit(1);
    }

    //after using pipe, you should also close the writing end of the pipe
    //pipe is now completely closed
    if (close(fd[0])==-1){
        perror("close pipe");
        exit(1);
    }

    //substitute the validate program with this one, no command line arguments
    //everthing after the execl() will not run! it is completely replaced by the
    //new program!
    execl("./validate","validate",NULL);
    perror("exec");
    return 1;//execl() failed

  }else{//fork failed

    perror("fork");
    exit(1);

  }
  return 0;
}
