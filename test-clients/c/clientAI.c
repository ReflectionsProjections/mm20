/*
** Part of the testclient for mechmania 20
**
** The purpose of this class is to handle the decision-making for each turn of the game
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include "AIObjects.c"

//Given name, set up initial message
char * init(char * name){
    char * str = malloc(150);
    return strcpy(str, "{\"team\":\"test\", \"members\":[{\"name\":\"test1\", \"archetype\":\"Coder\"},{\"name\":\"test2\", \"archetype\":\"Architect\"},{\"name\":\"test3\", \"archetype\":\"Theorist\"}]}");
}

//Given necessary info, put the turn into buf
//
int getTurn(char * buf, int turn, int id, ai * my_ai, member * members, room * rooms, response * responses){
    return 0;
}