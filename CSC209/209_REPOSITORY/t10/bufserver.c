#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#include "socket.h"

#ifndef PORT
  #define PORT 57552
#endif

#define BUFSIZE 30

int find_network_newline(const char *buf, int n);


int main() {
    // This line causes stdout not to be buffered.
    // Don't change this! Necessary for autotesting.
    setbuf(stdout, NULL);


    //precondition是每句话不超过30个character
    struct sockaddr_in *self = init_server_addr(PORT);
    int listenfd = setup_server_socket(self, 5);

    while (1) {
        int fd = accept_connection(listenfd);
        if (fd < 0) {
            continue;
        }

        // Receive messages
        char buf[BUFSIZE] = {'\0'};//很大很大的一个容器
        int inbuf = 0;           // How many bytes currently in buffer?
        int room = sizeof(buf);  // How many bytes remaining in buffer?
        char *after = buf;       // Pointer to position after the data in buf
        //char *after = buf[0]; 当前读取位置

        int nbytes;
        //那边可能给我传了很多句话
        //我们次能够读取的规模只能是一句话
        while ((nbytes = read(fd, after, room)) > 0) {//这里after下一次就是where了
            // Step 1: update inbuf (how many bytes were just added?)
            inbuf += nbytes;

            int where;

            // Step 2: the loop condition below calls find_network_newline
            // to determine if a full line has been read from the client.
            // Your next task should be to implement find_network_newline
            // (found at the bottom of this file).
            //
            // Note: we use a loop here because a single read might result in
            // more than one full line.

            //只要没读完，find_network_newline返回-1，没找到new line character
            //while不执行，回去上面那个while继续读
            while ((where = find_network_newline(buf, inbuf)) > 0) {
                // Step 3: Okay, we have a full line. 读到换行符了
                // Output the full line, not including the "\r\n",
                // using print statement below.
                // Be sure to put a '\0' in the correct place first;
                // otherwise you'll get junk in the output.
                // (Replace the "\r\n" with appropriate characters so the
                // message prints correctly to stdout.)

                buf[where-2] = '\0';
                printf("Next message: %s\n", buf);
                // Note that we could have also used write to avoid having to
                // put the '\0' in the buffer. Try using write later!

                // Step 4: update inbuf and remove the full line from the buffer
                // There might be stuff after the line, so don't just do inbuf = 0.
                inbuf -= where;//剩下还有多少个char没查

                //前where个元素已经全部print过了
                //where相当于下一句话的开始

                /*
                for (int i = 0; i < where-1; ++i)
                {
                    buf[i] = '\0';
                    //之前我们在第一位放一个’\0‘就整行变成\0是因为
                    //print或read function只会读到第一个\0
                    //但现在我们是一个一个读的，如果你只在第一位放\0
                    //他剩下的其他char还是会存在junk的
                }

                // You want to move the stuff after the full line to the beginning
                // of the buffer.  A loop can do it, or you can use memmove.
                // memmove(destination, source, number_of_bytes)
                */
                memmove(buf,buf+where,inbuf);

            }
            // Step 5: update after and room, in preparation for the next read.
            after = buf+inbuf;//读到现已有的content后面
            room = BUFSIZE - inbuf;


        }
        close(fd);
    }

    free(self);
    close(listenfd);
    return 0;
}


/*
 * Search the first n characters of buf for a network newline (\r\n).
 * Return one plus the index of the '\n' of the first network newline,
 * or -1 if no network newline is found.
 * Definitely do not use strchr or other string functions to search here. (Why not?)
 */
int find_network_newline(const char *buf, int inbuf) {
    for (int i = 0; i < inbuf-1; i++){//只能到inbuf-1因为要保证\r后面还要\n
        if (buf[i] == '\r' && buf[i+1] == '\n'){
            return i+2;//\n的index
        }
    }
    return -1;
}
