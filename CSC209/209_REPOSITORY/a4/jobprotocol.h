#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdarg.h>
#include <errno.h>


#ifndef __JOB_PROTOCOL_H__
#define __JOB_PROTOCOL_H__

#ifndef PORT
  #define PORT 55555
#endif

#ifndef MAX_JOBS
    #define MAX_JOBS 32
#endif

#define QUEUE_LENGTH 5
#define MAX_CLIENTS 20


// No paths or lines may be larger than the BUFSIZE below
#define BUFSIZE 256

#define CMD_INVALID -1
typedef enum {CMD_LISTJOBS, CMD_RUNJOB, CMD_KILLJOB, CMD_WATCHJOB, CMD_EXIT} JobCommand;
static const int n_job_commands = 5;
// See here for explanation of enums in C: https://www.geeksforgeeks.org/enumeration-enum-c/

typedef enum {NEWLINE_CRLF, NEWLINE_LF} NewlineType;

#define PIPE_READ 0
#define PIPE_WRITE 1

/*
You’re searching for the first network newline \r\n in your buffer, 
which indicates the end of the message that’s 
“waiting at the front of your buffer to be consumed”.
*/

struct cmd_detail {
	int pid;
	char jobname[BUFSIZE];
	char *argv[10];
};
typedef struct cmd_detail CmdDetail;


struct job_buffer {
	//(because you might have multiple messages or lines of output stored 
	//one after another inside your buffer, waiting to be read/consumed).
	char buf[BUFSIZE];
	int consumed;//consumed is the number of bytes that you are removing from your buffer
	int inbuf;//inbuf is the number of bytes that are currently stored inside your buffer
};
typedef struct job_buffer Buffer;

struct client {
	int socket_fd;
	struct job_buffer *buffer;
};
typedef struct client Client;

struct job_node {
	int pid;
	int stdout_fd;
	int stderr_fd;
	int dead;
	int wait_status;
	struct job_buffer *stdout_buffer;
	struct job_buffer *stderr_buffer;
	struct client *original_client;
	struct job_node *next;
};
typedef struct job_node JobNode;


struct job_list {
	struct job_node *first;
	int count;
};
typedef struct job_list JobList;


/* Returns the specific JobCommand enum value related to the
 * input str. Returns CMD_INVALID if no match is found.
 */
JobCommand get_job_command(char *,CmdDetail*);

/* Forks the process and launches a job executable. Allocates a
 * JobNode containing PID, stdout and stderr pipes, and returns
 * it. Returns NULL if the JobNode could not be created.
 */
JobNode* start_job(char *, char * const[]);

/* Adds the given job to the given list of jobs.
 * Returns 0 on success, -1 otherwise.
 */
int add_job(JobList*, JobNode*);

/* Sends SIGKILL to the given job_pid only if it is part of the given
 * job list. Returns 0 if successful, 1 if it is not found, or -1 if
 * the kill command failed.
 */
int kill_job(JobList*, int);

/* Removes a job from the given job list and frees it from memory.
 * Returns 0 if successful, or -1 if not found.
 */
int remove_job(JobList*, int);

/* Marks a job as dead.
 * Returns 0 on success, or -1 if not found.
 */
int mark_job_dead(JobList*, int, int);

/* Frees all memory held by a job list and resets it.
 * Returns 0 on success, -1 otherwise.
 */
int empty_job_list(JobList*);

/* Frees all memory held by a job node and its children.
 */
int delete_job_node(JobNode*);

/* Kills all jobs. Return number of jobs in list.
 */
int kill_all_jobs(JobList *);

/* Sends a kill signal to the job specified by job_node.
 * Return 0 on success, 1 if job_node is NULL, or -1 on failure.
 */
int kill_job_node(JobNode *);

/* Replaces the first '\n' or '\r\n' found in str with a null terminator.
 * Returns the index of the new first null terminator if found, or -1 if
 * not found.
 */
int remove_newline(char *, int);

/* Replaces the first '\n' found in str with '\r', then
 * replaces the character after it with '\n'.
 * Returns 1 + index of '\n' on success, -1 if there is no newline,
 * or -2 if there's no space for a new character.
 */
int convert_to_crlf(char*, int);

/* Search the first n characters of buf for a network newline (\r\n).
 * Return one plus the index of the '\n' of the first network newline,
 * or -1 if no network newline is found.
 */
int find_network_newline(const char *, int);

/* Search the first n characters of buf for an unix newline (\n).
 * Return one plus the index of the '\n' of the first network newline,
 * or -1 if no network newline is found.
 */
int find_unix_newline(const char *, int);

/* Read as much as possible from file descriptor fd into the given buffer.
 * Returns number of bytes read, or 0 if fd closed, or -1 on error.
 */
int read_to_buf(int, Buffer*);

/* Returns a pointer to the next message in the buffer, sets msg_len to
 * the length of characters in the message, with the given newline type.
 * Returns NULL if no message is left.
 */
char* get_next_msg(Buffer*, int*, char **);


/* Returns 1 if buffer is full, 0 otherwise.
 */
int is_buffer_full(Buffer *);

/*
 *  Client management
 */

/* Accept a connection and adds them to list of clients.
 * Return the new client's file descriptor or -1 on error.
 */
int setup_new_client(int listen_fd, Client *clients);

/* Closes a client and removes it from the list of clients.
 * Return the highest fd between all clients.
 */
int remove_client(int listen_fd, int client_index, Client *clients, JobList *job_list);

/* Read message from client and act accordingly.
 * Return their fd if it has been closed or 0 otherwise.
 */
int process_client_request(Client *client, JobList *job_list);

/*
 *  Sending to client
 */

/* Write a string to a client.
 * Returns 0 on success, 1 on failed/incomplete write, or -1 in case of error.
 */
int write_buf_to_client(int client_fd, char *buf, int buflen);


/* Print message to stdout, and send network-newline message to a client.
 * Returns 0 on success, 1 on failed/incomplete write, or -1 in case of error.
 */
int announce_buf_to_client(int client_fd, char *buf, int buflen);


/* Print string to stdout, and send network-newline string to a client.
 * Returns 0 on success, 1 on failed/incomplete write, 2 if the string
 * is too large, or -1 in case of error.
 */
int announce_str_to_client(int client_fd, char* str);

/* Print formatted string to stdout, and send network-newline string to a client.
 * Returns 0 on success, 1 on failed/incomplete write, 2 if the string
 * is too large, or -1 in case of error.
 */
int announce_fstr_to_client(int client_fd, const char *format, ...);


/*
 *  Childcare
 */

/* Process output from each child, remove them if they are dead, announce to watchers.
 * Returns 1 if at least one child exists, 0 otherwise.
 */
int process_job(JobList *job_list, int pid);


/* Read characters from fd and store them in buffer. Announce each message found
 * to watchers of job_node with the given format, eg. "[JOB %d] %s\n".
 */
int process_job_output(JobNode *job_node, int fd, Buffer *buffer, char *format);

/* Remove all dead children from job list, announce to watchers.
 * Returns count of dead jobs removed.
 */
int process_dead_children(JobList *job_list);

/* Remove the given child from the job list, announce to watchers.
 * Returns the next node that the job pointed to.
 */
int process_dead_child(JobList *job_list, JobNode *dead_job);

/*
 *  Misc
 */

/* Return the highest fd between all clients and job pipes.
 */
int get_highest_fd(int listen_fd, Client *clients);

/* Frees up all memory and exits.
 */
void clean_exit(int listen_fd, Client *clients, JobList *job_list, int exit_status);


#endif
