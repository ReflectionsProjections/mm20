

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
    SPY
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
    action_enum_t acted;
    int /*bool*/ asleep;
    float fatigue;
    float hunger;
    int /*bool*/ sitting;
    char * room_id;
    char * name;
    int team;
    int person_id;
    archetype_enum_t archetype;
    stats_t stats;
} person_t;

typedef struct {
    char * room_id;
    char ** connected_rooms;
    int num_connected_rooms;
    person_t * people;
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
    ai_stats_t stats;
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
    char * room_id;
} action_t;

typedef struct {
    action_t * actions;
    int num_actions;
} sent_turn_t;


void free_sent_turn(sent_turn_t * sent_turn) {
    int i;
    for (i = 0; i < sent_turn->num_actions; i++) {
        free(sent_turn->actions[i].room_id);
    }
    free(sent_turn->actions);
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
        free_people(received_turn->rooms[i].people, received_turn->rooms[i].num_people);
        free(received_turn->rooms[i].resources);
        for (j = 0; j < received_turn->rooms[i].num_connected_rooms; j++) {
            received_turn->rooms[i].connected_rooms[j];
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
}

#endif
