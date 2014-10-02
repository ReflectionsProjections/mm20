/*
** Part of the testclient for mechmania 20
**
** The purpose of this file is to contain data formats for communicating with the server.
*/

#ifndef AI_OBJECTS_T
#define AI_OBJECTS_T

typedef enum {
    MOVE,
    EAT,
    DISTRACT,
    SLEEP,
    CODE,
    THEORIZE,
    VIEW,
    WAKE_UP,
    SPY,
    DISTRACTED,
    NO_ACTION
} action_enum_t;

typedef enum {
    DEPLETED_SNACK_TABLE,
    PROFESSOR_ARRIVED,
    NO_PROFESSOR,
    PRACTICE
} event_enum_t;

typedef enum {
    CODER,
    THEORIST,
    ARCHITECT,
    INFORMANT
} archetype_enum_t;

typedef enum {
    IMPLEMENT,
    TEST,
    REFACTOR,
    OPTIMIZE
} code_enum_t;

typedef enum {
    FOOD,
    PROFESSOR,
    PROJECTOR
} resource_enum_t;

typedef struct {
    float complexity;
    float implementation;
    float optimization;
    float stability;
    float theory;
} ai_stats_t;

typedef struct {
    int coding;
    int optimize;
    int refactor;
    int spy;
    int test;
    int theorize;
} stats_t;

typedef struct {
    int person_id;
    int team;
    char * name;

    // optional fields
    char * room_id;
    action_enum_t acted;
    float fatigue;
    float hunger;
    int /*bool*/ asleep;
    int /*bool*/ sitting;
    archetype_enum_t archetype;
    stats_t stats;
} person_t;

typedef struct {
    char * room_id;
    char ** connected_rooms;
    int num_connected_rooms;
    int * people_ids;
    int num_people;
    resource_enum_t * resources;
    int num_resources;
} room_t;

typedef struct {
    char * action;
    char * message;
    char * reason;
    int /*bool*/ success;
} message_t;

typedef struct {
    event_enum_t name;
    char * room_id;
} event_t;

typedef struct {
    ai_stats_t ai_stats;
    char ** errors;
    int num_errors;
    person_t * people;
    int num_people;
    room_t * rooms;
    int num_rooms;
    message_t * messages;
    int num_messages;
    event_t * events;
    int num_events;
} received_turn_t;

typedef struct {
    action_enum_t action;
    int person_id;
    int victim;
    code_enum_t type;
    // while optional, make sure this is NULL if you don't use it so it gets freed correctly
    char * room_id;
} action_t;

typedef struct {
    action_t * actions;
    int num_actions;
} sent_turn_t;

typedef struct {
    archetype_enum_t archetype;
    char * name;
} member_t;

typedef struct {
    char * team_name;
    member_t * members;
    int num_members;
} initial_sent_t;

typedef struct {
    int /*bool*/ success;
    char ** errors;
    int num_errors;
    person_t * team_members;
    int num_team_members;
    char * team_name;
    int team_id;
    int turns_per_hour;
} initial_received_t;


void free_sent_turn(sent_turn_t * sent_turn) {
    int i;
    for (i = 0; i < sent_turn->num_actions; i++) {
        free(sent_turn->actions[i].room_id);
    }
    free(sent_turn->actions);
    free(sent_turn);
}

/**
 * Exodus 9:1
 */
void free_people(person_t * people, int num_people) {
    int i;
    for (i = 0; i < num_people; i++) {
        free(people[i].room_id);
        free(people[i].name);
    }
    free(people);
}

void free_initial_sent(initial_sent_t * sent) {
    int i;
    for (i = 0; i < sent->num_members; i++) {
        free(sent->members[i].name);
    }
    free(sent->members);
    free(sent->team_name);
    free(sent);
}

void free_initial_received(initial_received_t * received) {
    int i;
    for (i = 0; i < received->num_errors; i++) {
        free(received->errors[i]);
    }
    free(received->errors);
    free(received->team_name);
    free_people(received->team_members, received->num_team_members);
    free(received);
}

void free_received_turn(received_turn_t * received_turn) {
    int i;
    for (i = 0; i < received_turn->num_errors; i++) {
        free(received_turn->errors[i]);
    }
    free(received_turn->errors);
    free_people(received_turn->people, received_turn->num_people);
    for (i = 0; i < received_turn->num_rooms; i++) {
        int j;
        free(received_turn->rooms[i].room_id);
        free(received_turn->rooms[i].people_ids);
        free(received_turn->rooms[i].resources);
        for (j = 0; j < received_turn->rooms[i].num_connected_rooms; j++) {
            free(received_turn->rooms[i].connected_rooms[j]);
        }
        free(received_turn->rooms[i].connected_rooms);
    }
    free(received_turn->rooms);
    for (i = 0; i < received_turn->num_messages; i++) {
        free(received_turn->messages[i].action);
        free(received_turn->messages[i].message);
        free(received_turn->messages[i].reason);
    }
    free(received_turn->messages);
    for (i = 0; i < received_turn->num_events; i++) {
        free(received_turn->events[i].room_id);
    }
    free(received_turn->events);
    free(received_turn);
}

#endif
