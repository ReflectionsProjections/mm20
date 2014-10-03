/*
** Part of the testclient for mechmania 20
**
** The purpose of this file is to handle the decision-making for each turn of the game
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include "ai_objects.c"
#include "utils.c"

initial_sent_t * get_initial_message() {
    initial_sent_t * send_turn = (initial_sent_t *) malloc(sizeof(initial_sent_t));
    send_turn->team_name = str_clone("Close2DaMetal");
    send_turn->num_members = 3;
    send_turn->members = (member_t *) malloc(send_turn->num_members * sizeof(member_t));
    send_turn->members[0].name = str_clone("MastaCode");
    send_turn->members[0].archetype = CODER;
    send_turn->members[1].name = str_clone("Builda");
    send_turn->members[1].archetype = ARCHITECT;
    send_turn->members[2].name = str_clone("TheSage");
    send_turn->members[2].archetype = THEORIST;

    return send_turn;
}

sent_turn_t * get_first_turn(initial_received_t * initial_received) {
    sent_turn_t * send_turn = (sent_turn_t *) malloc(sizeof(sent_turn_t));
    send_turn->actions = NULL;
    send_turn->num_actions = 0;
}

sent_turn_t * get_turn(received_turn_t * received_turn, int team_id, int num_team_members) {
    sent_turn_t * send_turn = (sent_turn_t *) malloc(sizeof(sent_turn_t));
    send_turn->actions = (action_t *) malloc(num_team_members * sizeof(action_t));
    int i;
    int team_ind = 0;
    for (i = 0; i < received_turn->num_people; i++) {
        // make sure theyre on our team
        if (received_turn->people[i].team != team_id) {
            continue;
        }
        send_turn->actions[team_ind].action = MOVE;
        send_turn->actions[team_ind].person_id = received_turn->people[i].person_id;

        // get room player is currently in
        char * current_room_id = received_turn->people[i].room_id;
        room_t * room = NULL;
        int j;
        for (j = 0; j < received_turn->num_rooms; j++) {
            if (!strcmp(received_turn->rooms[j].room_id, current_room_id)) {
                room = &received_turn->rooms[j];
                break;
            }
        }

        //randomly select an adjacent room and go there.
        int rand_room_ind = rand() % room->num_connected_rooms;
        send_turn->actions[team_ind].room_id = str_clone(room->connected_rooms[rand_room_ind]);
        team_ind++;
    }
    send_turn->num_actions = num_team_members;
    return send_turn;
}
