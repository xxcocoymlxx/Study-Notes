// TODO: Use this file for helper functions (especially those you want available)
// to both executables.
#include "jobprotocol.h"


#ifndef JOBS_DIR
    #define JOBS_DIR "jobs/"
#endif

/* Returns the specific JobCommand enum value related to the
 * input str. Returns CMD_INVALID if no match is found.
 */
JobCommand get_job_command(char *next_command, CmdDetail *cmddetail){
	//jobsZ是invalid，jobs是valid的
	if ((strchr(next_command,'/'))!= NULL) return CMD_INVALID;
	else if(strncmp(next_command, "exit", 4) == 0){
		if(strlen(next_command)>4) return CMD_INVALID;
		else return CMD_EXIT;
	} 
	else if (strncmp(next_command, "jobs", 4) == 0){
		if (strlen(next_command)>4) return CMD_INVALID;
		else return CMD_LISTJOBS;
	} 
	else if(strncmp(next_command, "run ", 4) == 0){
		if (strlen(next_command)>BUFSIZE) return CMD_INVALID;
		memmove(next_command, next_command+4, strlen(next_command));//run现在已经被吃掉了

		int num_space = 0;
        for (int i = 0; i < strlen(next_command); ++i)
        {
            if (next_command[i] == ' ') num_space++;
        }

        if (num_space == 0){
        	cmddetail->argv[0] = next_command;
        	cmddetail->argv[1] = NULL;

        	char temp[BUFSIZE];
        	sprintf(temp, "%s%s", JOBS_DIR, next_command);//null terminating

       		strncpy(cmddetail->jobname,temp,strlen(temp));
       		cmddetail->jobname[strlen(temp)] = '\0';

        }else{
        	//num_space = 3
        	//run已经被吃掉了  fastjob arg1 arg2 arg3
            char *token = NULL;
            char *remaining = NULL;
            token = strtok_r(next_command, " ", &remaining);

            int i = 0;
            while (token){
                cmddetail->argv[i] = token;
                i++;
                token = strtok_r(NULL, " ", &remaining);//让他继续循环的
            }
            cmddetail->argv[num_space+1] = NULL;

            //此时temp[0]一定是jobname
            char temp_jobname[BUFSIZE];
            sprintf(temp_jobname, " %s%s", JOBS_DIR, cmddetail->argv[0]);//null terminating
            strncpy(cmddetail->jobname,temp_jobname,strlen(temp_jobname));
            cmddetail->jobname[strlen(temp_jobname)] = '\0';
        }
		return CMD_RUNJOB;
	} else if (strncmp(next_command, "kill ", 5) == 0) {
		if (strlen(next_command)>BUFSIZE) return CMD_INVALID;
		memmove(next_command, next_command+5, strlen(next_command));
		cmddetail->pid = strtol(next_command, NULL, 10);
		return CMD_KILLJOB;
	}else if (strncmp(next_command, "watch ", 6) == 0) {
		if (strlen(next_command)>BUFSIZE) return CMD_INVALID;
		memmove(next_command, next_command+6, strlen(next_command));
		cmddetail->pid = strtol(next_command, NULL, 10);
		return CMD_WATCHJOB;
	}else return CMD_INVALID;
}

/* Forks the process and launches a job executable. Allocates a
 * JobNode containing PID, stdout and stderr pipes, and returns
 * it. Returns NULL if the JobNode could not be created.
 * about 70 lines.
 */
//note： 这里传给你的就已经是jobname和arguments了，不用我们自己再parse了
JobNode* start_job(char *jobname, char *const argv[]){

	struct stat st;
	if (lstat(jobname,&st)<0) return NULL;

    //creating the stdout and stderr pipe
	int stdout_pipe[2], stderr_pipe[2];
	if ((pipe(stdout_pipe) == -1)|| (pipe(stderr_pipe) == -1)){
		perror("pipe");
		exit(1);
	}

	JobNode *jn = malloc(sizeof(JobNode));
  	jn->pid = -1;
  	jn->stdout_fd = stdout_pipe[PIPE_READ];
  	jn->stderr_fd = stderr_pipe[PIPE_READ];
	jn->dead = 0;//not dead yet
	jn->wait_status = 0;

	Buffer *stdout_buf = malloc(sizeof(Buffer));
	stdout_buf-> consumed = 0;
	stdout_buf-> inbuf = 0;

	Buffer *stderr_buf = malloc(sizeof(Buffer));
	stderr_buf-> consumed = 0;
	stderr_buf-> inbuf = 0;

	jn->stdout_buffer = stdout_buf;
	jn->stderr_buffer = stderr_buf;
	jn->original_client = NULL;
	jn->next = NULL;

	int r = fork();

  	if (r > 0){//parent process

  		if ((close(stdout_pipe[PIPE_WRITE])==-1) || (close(stderr_pipe[PIPE_WRITE])==-1)){
  			perror("close pipe");
  			return NULL;
  		}
  		jn->pid = r;
  		

	    return jn;	

    }else if(r == 0){//child process

    	if ((close(stdout_pipe[PIPE_READ])==-1) || (close(stderr_pipe[PIPE_READ])==-1)){
    		perror("close pipe");
    		return NULL;
    	}

    	if ((dup2(stdout_pipe[PIPE_WRITE],fileno(stdout))==-1)|| (dup2(stderr_pipe[PIPE_WRITE],fileno(stderr))==-1)){
    		perror("dup2");
    		return NULL;
    	}

    	execvp(jobname,argv);
    	perror("execvp");
    	//*(JOB 22606)* execvp: No such file or directory
    	return NULL;//execl() failed

  }else{//fork failed
  	close(stdout_pipe[PIPE_WRITE]);
  	close(stdout_pipe[PIPE_READ]);
  	close(stderr_pipe[PIPE_WRITE]);
  	close(stderr_pipe[PIPE_READ]);
  	free(jn->stdout_buffer);
  	free(jn->stderr_buffer);
  	free(jn);
  	perror("fork");
  	return NULL;
  }
}

/* Adds the given job to the given list of jobs.
 * Returns 0 on success, -1 otherwise.
 */
int add_job(JobList* joblist, JobNode* jobnode){

	JobNode *curr = joblist->first;
	if (curr == NULL){
		joblist->first = jobnode;
		joblist->count++;
		return 0;
	}

	while(curr->next != NULL){
		curr = curr->next;
	}
	//reached the end of the linked list
	curr->next = jobnode;
	joblist->count++;
	return 0;
}

/* Removes a job from the given job list and frees it from memory.
 * Returns 0 if successful, or -1 if not found.
 */
int remove_job(JobList* joblist, int pid){
	if (joblist->count == 0) return -1;//没啥好remove的

	//删除第一个的情况
	if (joblist->first->pid == pid){
		JobNode *first = joblist->first;
		joblist->first = first->next;
		first->next = NULL;
		//free first
		delete_job_node(first);
		joblist->count--;
		return 0;
	}

	//删除的是后面的情况
	JobNode *curr = joblist->first;
	while(curr->next != NULL){
		if (curr->next->pid == pid){
			JobNode *new = curr->next;
			curr->next = new->next;
			new->next = NULL;
			//free new
			delete_job_node(new);
			joblist->count--;
			return 0;
		}
		curr = curr->next;
	}

	//如果出了这个while loop这个function还没有结束，就说没有找到我们要删除的node
	return -1;
}

/* Marks a job as dead.
 * Returns 0 on success, or -1 if not found.
 */
int mark_job_dead(JobList* joblist, int wait_status, int pid){
	if (joblist->first == NULL) return -1;

	JobNode *curr = joblist->first;
	while(curr != NULL){
		if (curr->pid == pid){
			curr->dead = 1;//1 is true
			curr->wait_status = wait_status;
			return 0;
		}
		curr = curr->next;
	}
	//the node with pid is not in the joblist
	return -1;
}

/* Frees all memory held by a job list and resets it.
 * Returns 0 on success, -1 otherwise.
 */
int empty_job_list(JobList* joblist){
	if (joblist->first == NULL){
		free(joblist);
		return 0;
	}

	JobNode *head = joblist->first;
	JobNode *temp;

	while (head != NULL){
		temp = head;
		head = head -> next;
		temp -> next = NULL;
		delete_job_node(temp);
	}
	free(joblist);
	return 0;
}

/* Frees all memory held by a job node and its children.
 */
int delete_job_node(JobNode* jobnode){
	if (jobnode == NULL) return -1;
		close(jobnode->stdout_fd);
		close(jobnode->stderr_fd);
		free(jobnode->stdout_buffer);
		free(jobnode->stderr_buffer);
		free(jobnode);
	return 0;
}

/* Sends SIGKILL to the given job_pid only if it is part of the given
 * job list. Returns 0 if successful, 1 if it is not found, or -1 if
 * the kill command failed.
 */
int kill_job(JobList* joblist, int pid){

	JobNode *curr = joblist->first;

	while(curr != NULL){
		if (curr->pid == pid){
			return kill_job_node(curr);
		}
		curr = curr->next;
	}
	//job_pid is not in the jobs linked list
	return 1;
}

/* Kills all jobs. Return number of jobs in list.
 */
int kill_all_jobs(JobList * joblist){
	JobNode *head = joblist->first;
	JobNode *temp;

	while (head != NULL){
		temp = head;
		head = head -> next;
		temp -> next = NULL;
		if (kill(temp->pid, SIGKILL) == 0) joblist->count--;
	}
	return joblist->count;
}

/* Sends a kill signal to the job specified by job_node.
 * Return 0 on success, 1 if job_node is NULL, or -1 on failure.
 */
int kill_job_node(JobNode * jobnode){
	if (kill(jobnode->pid, SIGKILL) == 0) {
		announce_fstr_to_client(jobnode->original_client->socket_fd,"[Job %d] Exited due to signal.", jobnode->pid);
		return 0;
	}
	return -1;
}


/* 
				把'\n' or '\r\n'换成 \0
 * Replaces the first '\n' or '\r\n' found in str with a null terminator.
 * Returns the index of the new first null terminator if found, or -1 if
 * not found.
  Watch out, because you can’t assume that your buffer always contains 
  exactly 1 command or line of output (LOO). It might contain multiple 
  commands/LOO. Or it might even contain a fraction of a command/LOO 
  (in the case where TCP fragments your command/LOO into multiple segments, 
  so it gets delivered to your server one segment at a time).
 */

int remove_newline(char *buf, int inbuf){
	for (int i = 0; i < inbuf; ++i){
		if((buf[i] == '\n') && (buf[i-1] != '\r')){
			buf[i] = '\0';
			return i;
		}else if (buf[i] == '\r' && buf[i+1] == '\n'){
			buf[i] = '\0';
			buf[i+1] = '\0';
			return i;
		}
	}
    //如果上面两层都没结束的话，就是没找到
	return -1;
}

/* 
 					把'\n'换成'\r\n'
 * Replaces the first '\n' found in str with '\r', 
 * then replaces the character after it with '\n'.
 * Returns 1 + index of '\n' on success, -1 if there is no newline,
 * or -2 if there's no space for a new character.
 */
int convert_to_crlf(char *buf, int inbuf){
	if (inbuf == BUFSIZE) return -2;//there's no space for a new character.
	
	int index;

	if ((index = find_network_newline(buf,inbuf))!=-1){//return 1 + index of \n
		buf[index] = '\0';
		return index;
	}

	return -1;//there is no newline

	return index+1;

}

/* 
			return \r\n 之后的index
Search the first n characters of buf for a network newline (\r\n).
 * Return one plus the index of the '\n' of the first network newline,
 * or -1 if no network newline is found.
 */
int find_network_newline(const char *buf, int inbuf){
	for (int i = 0; i < inbuf-1; ++i)
	{
		if (buf[i] == '\r' && buf[i+1] == '\n') return i+2;
	}
	return -1;
}

/* 			return \n 之后的index
Search the first n characters of buf for an unix newline (\n).
 * Return 1 + the index of the '\n' of the first network newline,
 * or -1 if no network newline is found.
 */
int find_unix_newline(const char *buf, int n){
	for (int i = 0; i < n-1; ++i)
	{
		if (buf[i] == '\n') return i+1;
	}
	return -1;
}

/* Read as much as possible from file descriptor fd into the given buffer.
 * Returns number of bytes read, or 0 if fd closed, or -1 on error.
 */
int read_to_buf(int fd, Buffer* buffer){
	char *buf = buffer->buf;
 	int inbuf = buffer->inbuf;

 	int nbytes;
 	while((nbytes=read(fd,buf+inbuf,BUFSIZE))>0){
  		inbuf += nbytes;
  		if (inbuf>=BUFSIZE) {
  			buf[BUFSIZE-1] = '\0';
  			return 3;
  		}

  		int newline;
  		if((newline=find_network_newline(buf,inbuf))>0){
   			buffer->inbuf = inbuf;
   			buffer->consumed = newline;
   			return 0;
  		}
 	}
 	return -1;
}


/* Returns 1 if buffer is full, 0 otherwise.
 */
int is_buffer_full(Buffer *buffer){
	if (buffer->inbuf == BUFSIZE) return 1;
	else return 0;
}