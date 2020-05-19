#ifndef __JOB_PROTOCOL_H__
#define __JOB_PROTOCOL_H__

#ifndef PORT
  #define PORT 55555
#endif

#ifndef MAX_JOBS
    #define MAX_JOBS 32
#endif

// No paths or lines may be larger than the BUFSIZE below
#define BUFSIZE 256

#define CMD_INVALID -1
typedef enum {CMD_LISTJOBS, CMD_RUNJOB, CMD_KILLJOB, CMD_WATCHJOB, CMD_EXIT} JobCommand;
static const int n_job_commands = 5;
// See here for explanation of enums in C: https://www.geeksforgeeks.org/enumeration-enum-c/

typedef enum {NEWLINE_CRLF, NEWLINE_LF} NewlineType;

#define PIPE_READ 0
#define PIPE_WRITE 1

struct job_buffer {
	char buf[BUFSIZE];
	int consumed;
	int inbuf;
};
typedef struct job_buffer Buffer;

struct client {
	int socket_fd;
	struct job_buffer buffer;
};
typedef struct client Client;

struct watcher_node {
	int client_fd;
	struct watcher_node *next;
};
typedef struct watcher_node WatcherNode;

struct watcher_list {
	struct watcher_node* first;
	int count;
};
typedef struct watcher_list WatcherList;

struct job_node {
	int pid;
	int stdout_fd;
	int stderr_fd;
	int dead;
	int wait_status;
	struct job_buffer stdout_buffer;
	struct job_buffer stderr_buffer;
	struct watcher_list watcher_list;
	struct job_node* next;
};
typedef struct job_node JobNode;


struct job_list {
	struct job_node* first;
	int count;
};
typedef struct job_list JobList;

/* Returns the specific JobCommand enum value related to the
 * input str. Returns CMD_INVALID if no match is found.
 */
JobCommand get_job_command(char*);

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

/* Adds the given watcher to the given list of watchers.
 * Returns 0 on success, -1 otherwise.
 */
int add_watcher(WatcherList*, int);

/* Removes a watcher from the given watcher list and frees it from memory.
 * Returns 0 if successful, or 1 if not found.
 */
int remove_watcher(WatcherList*, int);

/* Removes a client from every watcher list in the given job list.
 */
void remove_client_from_all_watchers(JobList*, int);

/* Adds the given watcher to a given job pid.
 * Returns 0 on success, 1 if job was not found, or -1 if watcher could not
 * be allocated.
 */
int add_watcher_by_pid(JobList*, int, int);

/* Removes the given watcher from the list of a given job pid.
 * Returns 0 on success, 1 if job was not found, or 2 if client_fd could
 * not be found in list of watchers.
 */
int remove_watcher_by_pid(JobList*, int, int);

/* Frees all memory held by a watcher list and resets it.
 * Returns 0 on success, -1 otherwise.
 */
int empty_watcher_list(WatcherList *);

/* Frees all memory held by a watcher node and its children.
 */
int delete_watcher_node(WatcherNode *);

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
char* get_next_msg(Buffer*, int*, NewlineType);

/* Removes consumed characters from the buffer and shifts the rest
 * to make space for new characters.
 */
void shift_buffer(Buffer *);

/* Returns 1 if buffer is full, 0 otherwise.
 */
int is_buffer_full(Buffer *);

#endif
