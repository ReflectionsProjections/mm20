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
    free(name);
    send(sockfd, buf, strlen(buf), 0);

    char received_str[MAXDATASIZE];
    recv(sockfd, received_str, MAXDATASIZE - 1, 0);
    json_error_t json_error;
    json_t * initial_json_root = json_loads(received_str, 0, &json_error);
    initial_received_t * initial_received = json_to_initial_received(initial_json_root);
    int team_id = initial_received->team_id;
    int num_team_members = initial_received->num_team_members;
    printf("Team %i with %i members\n", team_id, num_team_members);
    json_decref(initial_json_root);

    sent_turn_t * first_turn = get_first_turn(initial_received);
    free_initial_received(initial_received);

    json_t * first_turn_json = sent_turn_to_json(first_turn);
    free_sent_turn(first_turn);

    char * initial_sent_str = json_dumps(first_turn_json, JSON_ENSURE_ASCII);
    json_decref(first_turn_json);
    if (!initial_sent_str) {
        fprintf(stderr, "error converting json to string");
        close(sockfd);
        return -1;
    }

    int first_sent_length = strlen(initial_sent_str);
    initial_sent_str[first_sent_length] = '\n';
    send(sockfd, initial_sent_str, first_sent_length + 1, 0);
    free(initial_sent_str);

    while (1) {
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

        json_t * received_json_root = json_loads(received_str, 0, &json_error);
        if (!received_json_root) {
            fprintf(stderr, "failed to load json from server\n");
            break;
        }

        received_turn_t * received_turn = json_to_received_turn(received_json_root);
        json_decref(received_json_root);

        sent_turn_t * sent_turn = get_turn(received_turn, team_id, num_team_members);
        free_received_turn(received_turn);

        json_t * sent_turn_json = sent_turn_to_json(sent_turn);
        free_sent_turn(sent_turn);

        char * sent_str = json_dumps(sent_turn_json, JSON_ENSURE_ASCII);
        json_decref(sent_turn_json);
        if (!sent_str) {
            fprintf(stderr, "error converting json to string");
            break;
        }

        int sent_length = strlen(sent_str);
        sent_str[sent_length] = '\n';
        send(sockfd, sent_str, sent_length + 1, 0);
        free(sent_str);
    }

    close(sockfd);

    return 0;
}

