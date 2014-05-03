/*
** Part of the testclient for mechmania 20
**
** The purpose of this class is to do the communications with the server, and parse the json into a form that we can use.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include "clientAI.c"


#define HOST "localhost"
#define PORT "8080"
#define MAXDATASIZE 4096

//code for loading a file
char *loadFile(char *filename)
{
    FILE* input = fopen(filename, "rb");
    if(input == NULL) return NULL;

    if(fseek(input, 0, SEEK_END) == -1) return NULL;
    long size = ftell(input);
    if(size == -1) return NULL;
    if(fseek(input, 0, SEEK_SET) == -1) return NULL;

    char *content =malloc( (size_t) size +1 );
    if(content == NULL) return NULL;

    fread(content, 1, (size_t)size, input);
    if(ferror(input)) {
        free(content);
        return NULL;
    }

    fclose(input);
    content[size] = '\0';
    return content;
}

//Credit to Beej's Guide
int sendall(int s, char *buf, int *len)
{
    int total = 0; // how many bytes we've sent
    int bytesleft = *len; // how many we have left to send
    int n;

    while(total < *len) {
        n = send(s, buf+total, bytesleft, 0);
        if (n == -1) { break; }
        total += n;
        bytesleft -= n;
    }

    *len = total; // return number actually sent here

    return n==-1?-1:0; // return -1 on failure, 0 on success
}

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}


int team_id(char * str){
    return 0;
}

//parse out ai stats
ai * aiStats(char * str){
    return 0;
}

//parse out team members
member * teamMembers(char * str){
    return 0;
}

//parse out errors
char ** errors(char * str){
    return 0;
}

//parse out rooms
room * map(char * str){
    return 0;
}

//parse out responses
response * responses(char * str){
    return 0;
}

//Receive all data from server (ends in \n)
int recvall(int sockfd, char * str){
    return 0;
}

int main(void)
{
    char * name=loadFile("name.txt");
    char * buf= init(name); //get starting message
    int sockfd, numbytes;
    struct addrinfo hints, *servinfo, *p;
    int rv;
    char s[INET6_ADDRSTRLEN];

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((rv = getaddrinfo(HOST, PORT, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    // loop through all the results and connect to the first we can
    for(p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
            p->ai_protocol)) == -1) {
            perror("client: socket");
            continue;
        }

        if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("client: connect");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "client: failed to connect\n");
        return 2;
    }

    inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
    s, sizeof s);

    freeaddrinfo(servinfo); // all done with this structure

    send(sockfd, buf, strlen(buf), 0);

    char str[MAXDATASIZE];
    if ((numbytes = recv(sockfd, str, MAXDATASIZE-1, 0)) == -1) {
        perror("recv");
        exit(1);
    }

    str[numbytes] = '\0';

    int res;
    int run = 1;

    while(run){
        res=getTurn(buf, 0, team_id(str), aiStats(str), teamMembers(str), map(str), responses(str));
        if(res==1) break;
        if(res==2) {
            send(sockfd, buf, strlen(buf)+1, 0);
        }

        printf("recv\n");
        if ((numbytes = recv(sockfd, str, MAXDATASIZE-1, 0)) == -1) {
            perror("recv");
            exit(1);
        }
        if (numbytes == 0){
            run = 0;
        }

        str[numbytes] = '\0';
    }

    close(sockfd);
    free(buf);
    //free(name);

    return 0;
}

