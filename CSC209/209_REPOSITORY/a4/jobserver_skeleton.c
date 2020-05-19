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

#include "socket.h"
#include "jobprotocol.h"

#define QUEUE_LENGTH 5
#define MAX_CLIENTS 20

#ifndef JOBS_DIR
    #define JOBS_DIR "jobs/"
#endif

// Global list of jobs
JobList job_list;

// Flag to keep track of SIGINT received
int sigint_received;

/* SIGINT handler:
 * We are just raising the sigint_received flag here. Our program will
 * periodically check to see if this flag has been raised, and any necessary
 * work will be done in main() and/or the helper functions. Write your signal 
 * handlers with care, to avoid issues with async-signal-safety.
 */
void sigint_handler(int code) {
    sigint_received = 1;
}

// TODO: SIGCHLD (child stopped or terminated) handler: mark jobs as dead
void sigchld_handler(int code);

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
int process_client_request(Client *client, JobList *job_list, fd_set *all_fds);

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
 *  Announcing to watchers. Remember: leave the watch feature to the end.
 */

/* Print message to stdout, and send network-newline message to a list of
 * clients. Returns 0 on success, 1 on failed/incomplete write, or -1 in
 * case of error.
 */
int announce_buf_to_watchers(WatcherList *watcher_list, char *buf, int buflen);

/* Print string to stdout, and send network-newline string to a list of
 * clients. Returns 0 on success, 1 on failed/incomplete write, 2 if the
 * string is too large, or -1 in case of error.
 */
int announce_str_to_watchers(WatcherList *watcher_list, char *str);

/* Print formatted string to stdout, and send network-newline string to a list of
 * clients. Returns 0 on success, 1 on failed/incomplete write, 2 if the string
 * is too large, or -1 in case of error.
 */
int announce_fstr_to_watchers(WatcherList *watcher_list, const char *format, ...);

/*
 *  Childcare
 */

/* Process output from each child, remove them if they are dead, announce to watchers.
 * Returns 1 if at least one child exists, 0 otherwise.
 */
int process_jobs(JobList *job_list, fd_set *current_fds, fd_set *all_fds);

/* Read characters from fd and store them in buffer. Announce each message found
 * to watchers of job_node with the given format, eg. "[JOB %d] %s\n".
 */
void process_job_output(JobNode *job_node, int fd, Buffer *buffer, char *format);

/* Remove all dead children from job list, announce to watchers.
 * Returns count of dead jobs removed.
 */
int process_dead_children(JobList *job_list, fd_set *all_fds);

/* Remove the given child from the job list, announce to watchers.
 * Returns the next node that the job pointed to.
 */
JobNode *process_dead_child(JobList *job_list, JobNode *dead_job, fd_set *all_fds);

/*
 *  Misc
 */

/* Return the highest fd between all clients and job pipes.
 */
int get_highest_fd(int listen_fd, Client *clients, JobList *job_list);

/* Frees up all memory and exits.
 */
void clean_exit(int listen_fd, Client *clients, JobList *job_list, int exit_status);

int main(void) {
    // Reset SIGINT received flag.
    sigint_received = 0;

    // This line causes stdout and stderr not to be buffered.
    // Don't change this! Necessary for autotesting.
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    // TODO: Set up SIGCHLD handler

    // TODO: Set up SIGINT handler

    // TODO: Set up server socket

    // TODO: Initialize client tracking structure (array list)

    // TODO: Initialize job tracking structure (linked list)

    // TODO: Set up fd set(s) that we want to pass to select()

    while (1) {
	// Use select to wait on fds, also perform any necessary checks 
	// for errors or received signals

        // Accept incoming connections

        // Check our job pipes, update max_fd if we got children

        // Check on all the connected clients, process any requests
	// or deal with any dead connections etc.
    }

    clean_exit(listen_fd, clients, &job_list, 0);
    return 0;
}
