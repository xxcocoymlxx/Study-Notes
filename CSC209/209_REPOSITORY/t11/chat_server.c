#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "socket.h"


#ifndef PORT
  #define PORT 57552
#endif
#define MAX_BACKLOG 5
#define MAX_CONNECTIONS 4
#define BUF_SIZE 128


struct sockname {
    int sock_fd;
    char *username;
};


/* Accept a connection. Note that a new file descriptor is created for
 * communication with the client. The initial socket descriptor is used
 * to accept connections, but the new socket is used to communicate.
 * Return the new client's file descriptor or -1 on error.
 */
int setup_new_client(int fd, struct sockname *usernames) {
    int user_index = 0;
    while (user_index < MAX_CONNECTIONS && usernames[user_index].sock_fd != -1) {
        user_index++;
    }

    int client_fd = accept_connection(fd);
    if (client_fd < 0) {
        return -1;
    }

    if (user_index >= MAX_CONNECTIONS) {
        fprintf(stderr, "server: max concurrent connections\n");
        close(client_fd);
        return -1;
    }


    usernames[user_index].sock_fd = client_fd;
    usernames[user_index].username = malloc(sizeof(char)*BUF_SIZE);//setting up the username for the new client


    //the first thing it reads from the client has to be the username
    int num_read = read(client_fd,usernames[user_index].username, BUF_SIZE);
    if (num_read < 0) return -1;//return -1 on error.
    usernames[user_index].username[num_read-1] = '\0';//这里设为-1是因为最后一位是’\n‘，我们不想换行，所以提前一位把他换成terminator

    
    return client_fd;
}


/* Read a message from client_index and echo it back to them.
 * Return the fd if it has been closed or 0 otherwise.
 */
int read_from(int client_index, struct sockname *usernames) {
    int fd = usernames[client_index].sock_fd;
    char buf[BUF_SIZE + 1];

    int num_read = read(fd, &buf, BUF_SIZE);//只从这个读
    buf[num_read] = '\0';
    //concatenate "Username:" in front of buf
    //这才是server要发给所有client看的message！下面那个print只是server自己print的！
    if (num_read == 0) return fd;

    int username_len = strlen(usernames[client_index].username);
    char message[BUF_SIZE];
    
    strncpy(message,usernames[client_index].username, username_len);
    message[username_len] = '\0';

    strncat(message,": ",sizeof(message)-strlen(message)-1);
    message[username_len+2] = '\0';

    strncat(message,buf,sizeof(message)-strlen(message)-1);
    message[strlen(buf)+2+username_len] = '\0';

    for (int i = 0; i < MAX_CONNECTIONS; ++i){
        if (usernames[i].sock_fd != -1){//make sure it is not -1 so it can write to it 
            int num_write = write(usernames[i].sock_fd,message, strlen(message));
            if (num_write != strlen(message)){
                usernames[client_index].sock_fd = -1;
                return fd;
            }
        }
    }
    return 0;
}


int main(void) {
    // This line causes stdout not to be buffered.
    // Don't change this! Necessary for autotesting.
    setbuf(stdout, NULL);

    struct sockaddr_in *self = init_server_addr(PORT);
    int sock_fd = setup_server_socket(self, MAX_BACKLOG);

    // Create a list of chat client users.
    struct sockname usernames[MAX_CONNECTIONS];
    for (int index = 0; index < MAX_CONNECTIONS; index++) {
        usernames[index].sock_fd = -1;
        usernames[index].username = NULL;
    }

    // The client accept - message accept loop. First, we prepare to listen to multiple
    // file descriptors by initializing a set of file descriptors.
    int max_fd;
    if (sock_fd >= fileno(stdin)) max_fd = sock_fd;
    else max_fd = fileno(stdin);

    fd_set all_fds, listen_fds;
    FD_ZERO(&all_fds);
    FD_SET(sock_fd, &all_fds);

    while (1) {
        // select updates the fd_set it receives, so we always use a copy and retain the original.
        listen_fds = all_fds;
        int nready = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("server: select");
            exit(1);
        }

        // Is it the original socket? Create a new connection ...
        if (FD_ISSET(sock_fd, &listen_fds)) {
            int client_fd = setup_new_client(sock_fd, usernames);
            if (client_fd < 0) {
                continue;
            }
            if (client_fd > max_fd) {
                max_fd = client_fd;
            }
            FD_SET(client_fd, &all_fds);
            printf("Accepted connection\n");
        }

        // Next, check the clients.
        // NOTE: We could do some tricks with nready to terminate this loop early.
        for (int index = 0; index < MAX_CONNECTIONS; index++) {
            if (usernames[index].sock_fd > -1 && FD_ISSET(usernames[index].sock_fd, &listen_fds)) {
                // Note: never reduces max_fd
                int client_closed = read_from(index, usernames);
                if (client_closed > 0) {
                    FD_CLR(client_closed, &all_fds);
                    close(client_closed);
                    printf("Client %d disconnected\n", client_closed);
                } else {
                    printf("Echoing message from client %d\n", usernames[index].sock_fd);
                }
            }
        }
    }

    // Should never get here.
    return 1;
}
