#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "socket.h"


#ifndef PORT
  #define PORT 57552
#endif
#define BUF_SIZE 128

int main(void) {
    int sock_fd = connect_to_server(PORT, "127.0.0.1");

    char buf[BUF_SIZE + 1];

    // Read input from the user, send it to the server, and then accept the
    // echo that returns. Exit when stdin is closed.
    int max_fd;
    if (sock_fd >= fileno(stdin)) max_fd = sock_fd;
    else max_fd = fileno(stdin);

    fd_set all_fds, listen_fds;
    FD_ZERO(&all_fds);//清空current set of file descriptors
    FD_SET(sock_fd, &all_fds);//add sock_fd to the current set of file descriptors
    FD_SET(fileno(stdin), &all_fds);//add stdin to the current set of file descriptors

    while (1) {

        listen_fds = all_fds;//copy current set of fds to a new set
        //因为select会destroy现有的set

        int nready = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("client: select");
            exit(1);
        }
        
        int num_read;
        //read from stdin
        if (FD_ISSET(fileno(stdin),&listen_fds)){//如果是从stdin读的
            num_read = read(fileno(stdin),&buf, BUF_SIZE);
            if (num_read == 0){
                break;
            }
            buf[num_read] = '\0';

            //I'm reading from the stdin, I have to send it to the server
            int num_written = write(sock_fd, buf, num_read);
            if (num_written != num_read) {
                perror("client: write");
                close(sock_fd);
                exit(1);
            }
            //prints any text it receives from the server on stdout
            //printf("Received from stdin: %s", buf);
        }

        //read from the socket
        if (FD_ISSET(sock_fd,&listen_fds)){//如果是从socket/file descriptors读的
            num_read = read(sock_fd ,&buf, BUF_SIZE);

            if (num_read == 0){
                break;
            }
            
            buf[num_read] = '\0';
            printf("%s", buf);
            
            //prints any text it receives from the server on stdout
            //printf("Received from server: %s", buf);
        } 
    }

    close(sock_fd);
    return 0;
}
