/*
** Part of the testclient for mechmania 20
**
** The purpose of this file is to do the communications with the server.
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
#include <jansson.h>

#include "client_ai.c"
#include "parse_json.c"
#include "utils.c"

#define HOST "localhost"
#define PORT "8080"
#define MAXDATASIZE 4096

int main() {
    char * name = load_file("name.txt");
    if (name == NULL) {
        fprintf(stderr, "could not load team name file\n");
        return -1;
    }
    int sockfd;
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
    for (p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
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
        return -1;
    }

    inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr), s, sizeof s);

    freeaddrinfo(servinfo); // all done with this structure

    char * buf = get_initial_message(name);
    send(sockfd, buf, strlen(buf), 0);

    char received_str[MAXDATASIZE];

    while (1) {
        printf("recv\n");
        int numbytes = recv(sockfd, received_str, MAXDATASIZE - 1, 0);
        if (numbytes == -1) {
            fprintf(stderr, "failed to recv");
            break;
        }
        if (numbytes == 0){
            fprintf(stderr, "server closed connection");
            break;
        }
        received_str[numbytes] = '\0';

        json_error_t error;
        json_t * received_json_root = json_loads(received_str, 0, &error);
        if (!received_json_root) {
            fprintf(stderr, "error: on line %d: %s\n", error.line, error.text);
            break;
        }

        received_turn_t * received_turn = json_to_received_turn(received_json_root);
        json_decref(received_json_root);

        sent_turn_t * sent_turn = get_turn(received_turn);
        free_received_turn(received_turn);

        json_t * sent_turn_json = sent_turn_to_json(sent_turn);
        free_sent_turn(sent_turn);

        char * sent_str = json_dumps(sent_turn_json, JSON_ENSURE_ASCII);
        json_decref(sent_turn_json);
        if (!sent_str) {
            fprintf(stderr, "error converting json to string");
            break;
        }

        send(sockfd, sent_str, strlen(sent_str) + 1, 0);
        free(sent_str);
    }

    close(sockfd);
    free(name);

    return 0;
}

