/*
** Part of the testclient for mechmania 20
**
** The purpose of this file is to hold utility functions.
*/

#ifndef UTILS_T
#define UTILS_T

//Credit to Beej's Guide
int sendall(int sockfd, char * buf, int * len) {
    int total = 0; // how many bytes we've sent
    int bytesleft = *len; // how many we have left to send
    int n;

    while(total < *len) {
        n = send(sockfd, buf+total, bytesleft, 0);
        if (n == -1) { break; }
        total += n;
        bytesleft -= n;
    }

    *len = total; // return number actually sent here

    return n==-1?-1:0; // return -1 on failure, 0 on success
}

//Receive all data from server (ends in \n)
int recvall(int sockfd, char * str) {
    return 0;
}

// get sockaddr, IPv4 or IPv6:
void * get_in_addr(struct sockaddr * sa) {
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

/**
 * Loads an entire file into a string
 */
char * load_file(char * filename) {
    FILE* input = fopen(filename, "rb");
    if (input == NULL) {
        return NULL;
    }

    if (fseek(input, 0, SEEK_END) == -1) {
        return NULL;
    }
    long size = ftell(input);
    if (size == -1) {
        return NULL;
    }
    if (fseek(input, 0, SEEK_SET) == -1) {
        return NULL;
    }

    char * content = malloc(size + 1);
    if (content == NULL) {
        return NULL;
    }

    fread(content, 1, size, input);
    if (ferror(input)) {
        free(content);
        return NULL;
    }

    fclose(input);
    content[size] = '\0';
    return content;
}

char * str_clone(const char * s) {
    char * s2 = (char *) malloc(strlen(s) + 1);
    strcpy(s2, s);
    return s2;
}

#endif
