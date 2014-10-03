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

#define MAXDATASIZE 32768

#define DEFAULT_HOST "localhost"
#define DEFAULT_PORT "8080"


void send_initial(int sockfd) {
    initial_sent_t * initial_sent = get_initial_message();
    json_t * initial_sent_json = initial_sent_to_json(initial_sent);
    free_initial_sent(initial_sent);

    char * initial_sent_str = json_dumps(initial_sent_json, JSON_ENSURE_ASCII);
    json_decref(initial_sent_json);

    int initial_sent_str_len = strlen(initial_sent_str);
    initial_sent_str[initial_sent_str_len] = '\n';

    send(sockfd, initial_sent_str, initial_sent_str_len + 1, 0);
    free(initial_sent_str);
}

initial_received_t * receive_initial(int sockfd, char * buffer) {
    int num_bytes = recv(sockfd, buffer, MAXDATASIZE - 1, 0);
    if (num_bytes == -1) {
        fprintf(stderr, "failed to recv\n");
        return NULL;
    }
    buffer[num_bytes] = '\0';

    json_t * initial_json_root = json_loads(buffer, 0, NULL);

    initial_received_t * initial_received = json_to_initial_received(initial_json_root);
    json_decref(initial_json_root);

    return initial_received;
}

int send_first_turn(int sockfd, sent_turn_t * first_turn) {
    json_t * first_turn_json = sent_turn_to_json(first_turn);
    free_sent_turn(first_turn);

    char * first_turn_str = json_dumps(first_turn_json, JSON_ENSURE_ASCII);
    json_decref(first_turn_json);
    if (!first_turn_str) {
        fprintf(stderr, "error converting json to string\n");
        return -1;
    }

    int first_sent_length = strlen(first_turn_str);
    first_turn_str[first_sent_length] = '\n';
    send(sockfd, first_turn_str, first_sent_length + 1, 0);
    free(first_turn_str);
    return 0;
}

received_turn_t * receive_turn(int sockfd, char * buffer) {
    int num_bytes = recv(sockfd, buffer, MAXDATASIZE - 1, 0);
    if (num_bytes == -1) {
        fprintf(stderr, "failed to recv\n");
        return NULL;
    }
    if (num_bytes == 0){
        fprintf(stderr, "server closed connection\n");
        return NULL;
    }
    buffer[num_bytes] = '\0';

    json_t * received_json_root = json_loads(buffer, 0, NULL);
    if (!received_json_root) {
        fprintf(stderr, "failed to load json from server\n");
        return NULL;
    }
    if (has_game_ended(received_json_root)) {
        json_decref(received_json_root);
        return NULL;
    }

    received_turn_t * received_turn = json_to_received_turn(received_json_root);
    json_decref(received_json_root);
    return received_turn;
}

int send_turn(int sockfd, sent_turn_t * sent_turn) {
    json_t * sent_turn_json = sent_turn_to_json(sent_turn);
    free_sent_turn(sent_turn);

    char * sent_str = json_dumps(sent_turn_json, JSON_ENSURE_ASCII);
    json_decref(sent_turn_json);
    if (!sent_str) {
        fprintf(stderr, "error converting json to string\n");
        return -1;
    }

    int sent_length = strlen(sent_str);
    sent_str[sent_length] = '\n';
    send(sockfd, sent_str, sent_length + 1, 0);
    free(sent_str);
    return 0;
}

int main(int argc, char * argv []) {
    char * ip, * port;
    if (argc == 3) {
        ip = argv[1];
        port = argv[2];
    } else {
        ip = DEFAULT_HOST;
        port = DEFAULT_PORT;
    }
    int sockfd = connect_to_server(ip, port);
    if (sockfd == -1) {
        fprintf(stderr, "failed to connect\n");
        return 0;
    }

    send_initial(sockfd);

    char received_str[MAXDATASIZE];
    initial_received_t * initial_received = receive_initial(sockfd, received_str);
    if (initial_received == NULL) {
        close(sockfd);
        return 0;
    }
    int team_id = initial_received->team_id;
    int num_team_members = initial_received->num_team_members;

    sent_turn_t * first_turn = get_first_turn(initial_received);
    free_initial_received(initial_received);

    send_first_turn(sockfd, first_turn);

    while (1) {
        received_turn_t * received_turn = receive_turn(sockfd, received_str);
        if (received_turn == NULL) {
            close(sockfd);
            return 0;
        }

        sent_turn_t * sent_turn = get_turn(received_turn, team_id, num_team_members);
        free_received_turn(received_turn);

        send_turn(sockfd, sent_turn);
    }

    close(sockfd);

    return 0;
}

