
#include "socket.h"
#include "jobprotocol.h"

// Global list of jobs
JobList *joblist;
Client clients[MAX_CLIENTS];

// Flag to keep track of SIGINT received
int sigint_received;
int server_fd;


/* SIGINT handler:
 * We are just raising the sigint_received flag here. Our program will
 * periodically check to see if this flag has been raised, and any necessary
 * work will be done in main() and/or the helper functions. Write your signal 
 * handlers with care, to avoid issues with async-signal-safety.
 */
void sigint_handler(int code) {

    sigint_received = 1;
    clean_exit(server_fd, clients, joblist, 0);
}

// TODO: SIGCHLD (child stopped or terminated) handler: mark jobs as dead
void sigchld_handler(int code){
    pid_t pid;
    int stat;
    while((pid=waitpid(-1,&stat,WNOHANG))>0){
        mark_job_dead(joblist, stat, pid);
        process_job(joblist, pid);
    }
}

/*
 *  Client management
 */

/* Accept a connection and adds them to list of clients.
 * Return the new client's file descriptor or -1 on error.
 */
int setup_new_client(int listen_fd, Client *clients){
    int user_index = 0;
    while (user_index < MAX_CLIENTS && clients[user_index].socket_fd != -1) {
        user_index++;
    }

    int client_fd = accept_connection(listen_fd);
    if (client_fd < 0) return -1;

    if (user_index >= MAX_CLIENTS) {
        fprintf(stderr, "[SERVER] MAX_CLIENTS exceeded\n");
        close(client_fd);
        return -1;
    }

    //在可以创建new client的位置initialize他
    clients[user_index].socket_fd = client_fd;
    //setting up the actual job struct for the new client
    clients[user_index].buffer = malloc(sizeof(Buffer));
    clients[user_index].buffer->inbuf = 0;
    clients[user_index].buffer->consumed = 0;
    
    return client_fd;

}


void clear_job_watcher(JobList *joblist, int client_closed){
    JobNode *curr = joblist->first;
    while(curr != NULL){
        if(curr->original_client->socket_fd == client_closed){
            curr->original_client = NULL;
        }
        curr = curr->next;
    }
}

/* Closes a client and removes it from the list of clients.
 * Return the highest fd between all clients.
   Return the highest fd between the listening socket and all active client sockets
   The joblist has to do with the minimal waiting 
 */


/* Read message from client and act accordingly.
 * Return their fd if it has been closed or 0 otherwise.
 * about 250 line
 * 从113行要写到363行
 */
int process_client_request(Client *client, JobList *joblist){

    char msg[BUFSIZE];
    int fd = client->socket_fd;
    Buffer *buffer = client->buffer;
    int PID;

    int foo;
    if ((foo = read_to_buf(fd,buffer) < 0))return fd;//if it has been closed
    if (foo == 3){
        strncat(msg,"[SERVER] Invalid command: ",26);
        strncat(msg,buffer->buf,BUFSIZE);
        msg[BUFSIZE-1] = '\0';
        announce_str_to_client(fd, msg);
        return fd;
    }
    
    CmdDetail *detail = malloc(sizeof(CmdDetail));
    detail->pid = 0;

    int r = 0;;
    char next_command[BUFSIZE] = {'\0'};

        int len;//Return 1 + the index of the '\n'
        //unix newline和network newline的位置不一样的！
        if ((len = find_network_newline(buffer->buf, buffer->inbuf))!= -1){
            r = remove_newline(buffer->buf, len);//return the index of the null terminator
            buffer->consumed = r+2;//现在前r个就已经被处理过了
            strncpy(next_command,buffer->buf,r+2);//copy第一个null terminator的位置前的东西去ptr里
            next_command[r] = '\0';
        }else if ((len = find_unix_newline(buffer->buf, buffer->inbuf))!= -1){
            r = remove_newline(buffer->buf, len);//return the index of the null terminator
            buffer->consumed = r+1;
            strncpy(next_command,buffer->buf,r+1);//copy第一个null terminator的位置前的东西去ptr里
            next_command[r] = '\0';
        }

        memmove(buffer->buf,(buffer->buf)+(buffer->consumed),buffer->inbuf);
        buffer->inbuf = (buffer->inbuf)-(buffer->consumed);
        buffer->consumed = 0;

        printf("[CLIENT %d] %s\n",client->socket_fd, next_command);

        int result;
        result = get_job_command(next_command,detail);

        switch(result){

            case CMD_INVALID:
            announce_fstr_to_client(fd, "[SERVER] Invalid command: %s", next_command);
            break;

            case CMD_LISTJOBS://jobs

            if (joblist->count == 0){
                strncpy(msg, "[SERVER] No currently running jobs",BUFSIZE);
                announce_str_to_client(fd, msg);
            }else{
                printf("currently job count:%d\n",joblist->count);
                //loop through the joblist and print the PID
                JobNode *curr = joblist->first;
                strncpy(msg, "[SERVER]",BUFSIZE);
                msg[9] = '\0';

                int msg_len;

                while(curr != NULL){
                    msg_len = strlen(msg);
                        //把joblist里的node的PID都粘贴到msg里
                    if (curr->dead != 1){
                            //把pid转成string,顺便一起加了空格
                        char str_pid[64];
                            sprintf(str_pid, " %d", curr->pid);//会自己null terminate的

                            int pid_len = strlen(str_pid);

                            strncat(msg,str_pid,pid_len+1);
                            msg[msg_len+pid_len] = '\0';
                            msg_len = strlen(msg);
                        }
                        curr = curr->next;
                    }//while loop ends, 已近收集到了所有PID
                    announce_str_to_client(fd,msg);
                }
                break;

            case CMD_RUNJOB://run jobname [arg]
            if (joblist->count < MAX_JOBS){
                JobNode *newjob = start_job(detail->jobname, detail->argv);
                if (newjob != NULL){
                    add_job(joblist, newjob);
                    newjob->original_client = client;
                    sprintf(msg, "[SERVER] Job %d created", newjob->pid);
                }else{
                    sprintf(msg, "[SERVER] No such file or directory");
                }
            }else{
                sprintf(msg, "[SERVER] MAXJOBS exceeded");
            }
            announce_str_to_client(fd, msg);
            break;

            case CMD_KILLJOB://kill pid

                PID = detail->pid;            

                int r = kill_job(joblist, PID);
                remove_job(joblist, PID);

                if (r == 1){   
                    sprintf(msg, "[SERVER] Job %d not found", PID);
                    msg[strlen(msg)+1] = '\n';
                    announce_str_to_client(fd, msg);
                }else if (r == -1){
                    //kill job failed, return the fd
                    return fd;
                }
            break;

            case CMD_WATCHJOB://watch pid
                 sprintf(msg, "[SERVER] Job %d not found", detail->pid);
                 announce_str_to_client(fd, msg);
                break;
            case CMD_EXIT://exit
                break;
            }//switch end
            free(detail);
            return 0;
    }//this function ends

/*  
 *  以下是Sending to client需要的function
 */

/* Write a string to a client.
 * Returns 0 on success, 1 on failed/incomplete write, or -1 in case of error.
 */
    int write_buf_to_client(int client_fd, char *buf, int buflen){
        int num_write = write(client_fd, buf, buflen);
        if (num_write < 0) return -1;
        if (num_write != buflen) return 1;
        return 0;
    }


/* Print string to stdout, and send network-newline string to a client.
 * Returns 0 on success, 1 on failed/incomplete write, 2 if the string
 * is too large, or -1 in case of error.
 -If the job prints "Hello\n" to stdout, the server sends "Hello\r\n" to the client, and the client prints out "Hello\n".
-If the job prints "Hello\r\n" to stdout, the server sends "Hello\r\r\n" to the client, and the client prints out "Hello\r\n".
 */
int announce_str_to_client(int client_fd, char* str){
    char copy[BUFSIZE];
    strncpy(copy,str,strlen(str));
    copy[strlen(str)] = '\0';
    remove_newline(copy, strlen(copy));//已经把output里的'\r\n'都换成\0了
    printf("%s\n",copy);


    int num_write = 0;
    int result = 0;
    result = convert_to_crlf(str, strlen(str));////Returns 1 + index of '\n'
    if (result < 0 ){
        strncat(str,"\r\n",2);
        num_write = write(client_fd,str,strlen(str));
    } else{
        //didn't find the \r\n
        num_write = write(client_fd,str,strlen(str));
    }

    
    if (num_write <0) return -1;
    else if ((num_write == 0) || (num_write != strlen(str))) return 1;
    return 0;
}

/* Print formatted string to stdout, and send network-newline string to a client.
 * Returns 0 on success, 1 on failed/incomplete write, 2 if the string
 * is too large, or -1 in case of error.
 * sample usage: 
 * announce_fstr_to_client(client_fd, "[SERVER] Unexpected argument: %s\n", cmd_args);
 */
int announce_fstr_to_client(int client_fd, const char *format, ...){
    va_list args;
    va_start(args, format);

    char msg[BUFSIZE + 1]; // vsnprintf will add a NULL terminator, so we need +1 byte
    vsnprintf(msg, BUFSIZE - 2, format, args); // need to make sure we have space for \r\n

    va_end(args);

    return announce_str_to_client(client_fd, msg);
}



/*
 *  以下是Childcare处理孩子需要的functions
 */

/* Process output from each child, remove them if they are dead, announce to watcher.
 * Returns 1 if at least one child exists, 0 otherwise.
 */
int process_job(JobList *job_list, int pid){
    JobNode *curr = job_list->first;

    while(curr!= NULL){

        if (curr->pid == pid)
        {
            process_job_output(curr, curr->stdout_fd, curr->stdout_buffer, "[JOB %d] %s");
            process_job_output(curr, curr->stderr_fd, curr->stderr_buffer, "*(JOB %d)* %s");
            process_dead_child(job_list, curr);
            return 0;
        }
        curr = curr->next;
    }

    return 0;
}


/* Read characters from fd and store them in buffer. Announce each message found
 * to watchers of job_node with the given format, eg. "[JOB %d] %s\n".
 */
int process_job_output(JobNode *job_node, int fd, Buffer *buffer, char *format){
    int num_read;
    num_read = read(fd,buffer->buf,BUFSIZE);
    if (num_read==0) return -1;

    if (num_read > 0 && num_read < BUFSIZE){
        buffer->buf[num_read] = '\0';
        announce_fstr_to_client(job_node->original_client->socket_fd, format, job_node->pid, buffer->buf);
    }else if(num_read >= BUFSIZE){
        announce_fstr_to_client(job_node->original_client->socket_fd,"*(SERVER)* Buffer from job %d is full. Aborting job.", job_node->pid);
    }
    return 0;
}

/* Remove all dead children from job list, announce to watchers.
 * Returns count of dead jobs removed.
 */
int process_dead_children(JobList *job_list){
    JobNode *curr = job_list->first;
    while(curr!=NULL){
        if(curr->dead == 1){
            announce_fstr_to_client(curr->original_client->socket_fd,"[JOB %d] Exited with status %d",curr->pid, curr->wait_status);
            remove_job(job_list, curr->pid);
        }
        curr=curr->next;
    }
    return 0;
}

/* Remove the given child from the job list, announce to watchers.
 * Returns the next node that the job pointed to.
 FD_CLR(fd, &fdset);
 */
int process_dead_child(JobList *job_list, JobNode *dead_job){
    JobNode *curr = job_list->first;
    while(curr!=NULL){
        if(curr->pid == dead_job->pid){
            announce_fstr_to_client(dead_job->original_client->socket_fd,"[JOB %d] Exited with status %d",dead_job->pid, dead_job->wait_status);
            remove_job(job_list, dead_job->pid);
            return 0;
        }
        curr = curr->next;
    }
    return -1;
}


/*
 *  Misc
 */

/* Return the highest fd between all clients and job pipes.
 */

int get_highest_fd(int listen_fd, Client *clients){
    //loop through the second list
    int max = listen_fd;
    for (int index = 0; index < MAX_CLIENTS; index++) {
        if (clients[index].socket_fd > max) max = clients[index].socket_fd;
    }
    return max;
}



/* Frees up all memory and exits.
 * close all of the client sockets (first) and then terminate all running jobs (second).
 * The clients should be sent the message "[SERVER] Shutting down"
 */
void clean_exit(int listen_fd, Client *clients, JobList *job_list, int exit_status){
    for (int index = 0; index < MAX_CLIENTS; index++) {
        if (clients[index].socket_fd != -1){
            announce_str_to_client(clients[index].socket_fd, "[SERVER] Shutting down");
            free(clients[index].buffer);
            close(clients[index].socket_fd);
        } 
    }
    kill_all_jobs(joblist);
    empty_job_list(joblist);
    close(listen_fd);
    exit(exit_status);
}



//about 100 lines
int main(void) {

    // Reset SIGINT received flag.
    sigint_received = 0;

    // This line causes stdout and stderr not to be buffered.
    // Don't change this! Necessary for autotesting.
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    
    
    // TODO: Set up SIGCHLD handler
    struct sigaction chld_act;
    sigemptyset(&chld_act.sa_mask); 
    chld_act.sa_flags = SA_RESTART;
    chld_act.sa_handler = sigchld_handler;
    if(sigaction(SIGCHLD, &chld_act, NULL)== -1) exit(1);

    
    // TODO: Set up SIGINT handler
    struct sigaction int_act;
    sigemptyset(&int_act.sa_mask); 
    int_act.sa_flags = SA_RESTART;
    int_act.sa_handler = sigint_handler;
    if (sigaction(SIGINT, &int_act, NULL) == -1) exit(1);
    

    // TODO: Set up server socket
    struct sockaddr_in *addr = init_server_addr(PORT);
    int sock_fd = setup_server_socket(addr, QUEUE_LENGTH); //QUEUE_LENGTH is 5
    server_fd = sock_fd;

    // TODO: Initialize client tracking structure (array list)
    // It’s an array of client structs
    for (int index = 0; index < MAX_CLIENTS; index++) {
        clients[index].socket_fd = -1;
        clients[index].buffer = NULL;
    }

    // TODO: Initialize job tracking structure (linked list)
    joblist = malloc(sizeof(JobList));
    joblist->first = NULL; //a struct pointing to a job node
    joblist->count = 0;

    // TODO: Set up fd set(s) that we want to pass to select()
    int max_fd = sock_fd;
    fd_set all_fds, listen_fds;
    FD_ZERO(&all_fds);
    FD_SET(sock_fd, &all_fds);

    /*
    Process here means see if any of the jobs have anything 
    to be read from their output pipes, read it, 
    and forward it to everyone who is listening to that job.

    You should have 2 copies of fd_set. One to pass into select() 
    (and it will get modified) and one to keep track of all the fds
     that need to be checked every iteration. So your loop should be something like this:
         while server is on:
            set current_fds to be a copy of all_fds
            find max fd in current_fds
            select(current_fds)
            do things with each fd in the current_fds

     Note: If you need to start checking on a new fd, you will need to add it to all_fds
    */


    while (1) {


        listen_fds = all_fds;

        // Use select to wait on fds, also perform any necessary checks 
        // for errors or received signals
        int r = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (r == -1) {
            continue;
        }

        // Accept incoming connections
        // Create a new connection
        if (FD_ISSET(sock_fd, &listen_fds)) {
            int client_fd = setup_new_client(sock_fd, clients);
            if (client_fd < 0){
                fprintf(stderr,"[SERVER] Client disconnected: max concurrent connections reached\n");
                continue;
            }
            if (client_fd > max_fd) max_fd = client_fd;
            FD_SET(client_fd, &all_fds);
            //printf("Accepted connection\n");
        }

        // Check our job pipes, update max_fd if we got children

        // Check on all the connected clients, process any requests
        // or deal with any dead connections etc.
        for (int index = 0; index < MAX_CLIENTS; index++) {
            if (clients[index].socket_fd > -1 && FD_ISSET(clients[index].socket_fd, &listen_fds)) {
                // Note: never reduces max_fd
                //现在是对clients进行循环处理

                int client_closed = process_client_request(&clients[index], joblist);//should return 0
                //这是同一个client，所以是写到同一个client的buf里
                //上面read_from的return value成功的话是0，失败的话是fd，which is 大于0
                
                if (client_closed > 0) {
                    FD_CLR(client_closed, &all_fds);
                    //clean up its data structures and then log the exit of the client with the message.

                    printf("[CLIENT %d] Connection closed\n",client_closed);
                    clients[index].socket_fd = -1;
                    memset(clients[index].buffer->buf,'\0',sizeof(char)*BUFSIZE);
                    clients[index].buffer->inbuf = 0;
                    clients[index].buffer->consumed = 0;
                    max_fd = get_highest_fd(sock_fd, clients);
                    clear_job_watcher(joblist, client_closed);
                    close(client_closed);
                }
            }
        }//for loop ends
    }
    //close all of the client sockets (first) and then terminate all running jobs (second).
    //The clients should be sent the message "[SERVER] Shutting down"
    clean_exit(sock_fd, clients, joblist, 0);
    return 0;
}
