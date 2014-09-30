/*
** Part of the testclient for mechmania 20
**
** The purpose of this file is to parse json into useful data structures.
*/

#ifndef PARSE_JSON_T
#define PARSE_JSON_T

#include <jansson.h>
#include "ai_objects.c"
#include "utils.c"

char ** json_to_string_array(json_t * json) {
    char ** strings = (char **) malloc(json_array_size(json) * sizeof(char *));
    int i;
    for (i = 0; i < json_array_size(json); i++) {
        json_t * json_s = json_array_get(json, i);
        strings[i] = str_clone(json_string_value(json_s));
    }
    return strings;
}

void json_to_person(json_t * person_json, person_t * person) {
    person->person_id = json_integer_value(json_object_get(person_json, "person_id"));
    person->team = json_integer_value(json_object_get(person_json, "team"));
    person->name = str_clone(json_string_value(json_object_get(person_json, "name")));

    if (!json_object_get(person_json, "sitting")) {
        person->room_id = NULL;
        return;
    }

    person->sitting = json_is_true(json_object_get(person_json, "sitting"));
    person->asleep = json_is_true(json_object_get(person_json, "asleep"));
    person->room_id = str_clone(json_string_value(json_object_get(person_json, "location")));

    json_t * acted_json = json_object_get(person_json, "acted");
    if (json_is_null(acted_json)) {
        person->acted = NO_ACTION;
    } else {
        const char * acted_s = json_string_value(acted_json);
        if (!strcmp(acted_s, "move")) {
            person->acted = MOVE;
        } else if (!strcmp(acted_s, "eat")) {
            person->acted = EAT;
        } else if (!strcmp(acted_s, "distract")) {
            person->acted = DISTRACT;
        } else if (!strcmp(acted_s, "sleep")) {
            person->acted = SLEEP;
        } else if (!strcmp(acted_s, "code")) {
            person->acted = CODE;
        } else if (!strcmp(acted_s, "theorizer")) {
            person->acted = THEORIZE;
        } else if (!strcmp(acted_s, "view")) {
            person->acted = VIEW;
        } else if (!strcmp(acted_s, "wake")) {
            person->acted = WAKE_UP;
        } else if (!strcmp(acted_s, "spy")) {
            person->acted = SPY;
        } else if (!strcmp(acted_s, "distracted")) {
            person->acted = DISTRACTED;
        }
    }

    if (!json_object_get(person_json, "fatigue")) {
        return;
    }

    person->fatigue = json_number_value(json_object_get(person_json, "fatigue"));
    person->hunger = json_number_value(json_object_get(person_json, "hunger"));

    json_t * stats_json = json_object_get(person_json, "stats");
    person->stats.coding = json_integer_value(json_object_get(stats_json, "coding"));
    person->stats.optimize = json_integer_value(json_object_get(stats_json, "optimize"));
    person->stats.refactor = json_integer_value(json_object_get(stats_json, "refactor"));
    person->stats.spy = json_integer_value(json_object_get(stats_json, "spy"));
    person->stats.test = json_integer_value(json_object_get(stats_json, "test"));
    person->stats.theorize = json_integer_value(json_object_get(stats_json, "theorize"));

    const char * arch_s = json_string_value(json_object_get(person_json, "archetype"));
    if (!strcmp(arch_s, "coder")) {
        person->archetype = CODER;
    } else if (!strcmp(arch_s, "theorist")) {
        person->archetype = THEORIST;
    } else if (!strcmp(arch_s, "architect")) {
        person->archetype = ARCHITECT;
    } else if (!strcmp(arch_s, "informant")) {
        person->archetype = INFORMANT;
    }
}

person_t * json_object_to_people(json_t * json) {
    person_t * people = (person_t *) malloc(json_object_size(json) * sizeof(person_t));
    const char * key;
    json_t * person_json;
    int i = 0;
    json_object_foreach(json, key, person_json) {
        json_to_person(person_json, people + i);
        i++;
    }
    return people;
}

room_t * json_to_rooms(json_t * json) {
    room_t * rooms = (room_t *) malloc(json_object_size(json) * sizeof(room_t));
    const char * key;
    json_t * room_json;

    int i = 0;
    int j;
    json_object_foreach(json, key, room_json) {
        rooms[i].room_id = str_clone(json_string_value(json_object_get(room_json, "room")));
        rooms[i].connected_rooms = json_to_string_array(json_object_get(room_json, "connectedRooms"));
        rooms[i].num_connected_rooms = json_array_size(json_object_get(room_json, "connectedRooms"));

        json_t * people_ids_json = json_object_get(room_json, "peopleInRoom");
        rooms[i].num_people = json_array_size(people_ids_json);
        rooms[i].people_ids = (int *) malloc(rooms[i].num_people * sizeof(int));
        for (j = 0; j < rooms[i].num_people; j++) {
            rooms[i].people_ids[j] = json_integer_value(json_array_get(people_ids_json, j));
        }

        rooms[i].num_resources = json_array_size(json_object_get(room_json, "resources"));
        rooms[i].resources = (resource_enum_t *) malloc(rooms[i].num_resources * sizeof(resource_enum_t));

        json_t * resources_json = json_object_get(room_json, "resources");
        for (j = 0; j < rooms[i].num_resources; j++) {
            const char * resource_s = json_string_value(json_array_get(resources_json, j));
            if (!strcmp(resource_s, "FOOD")) {
                rooms[i].resources[j] = FOOD;
            } else if (!strcmp(resource_s, "PROFESSOR")) {
                rooms[i].resources[j] = PROFESSOR;
            } else if (!strcmp(resource_s, "PROJECTOR")) {
                rooms[i].resources[j] = PROJECTOR;
            }
        }
        i++;
    }
    return rooms;
}

message_t * json_to_messages(json_t * json) {
    message_t * messages = (message_t *) malloc(json_array_size(json) * sizeof(message_t));
    int i;
    for (i = 0; i < json_array_size(json); i++) {
        json_t * message_json = json_array_get(json, i);
        messages[i].action = str_clone(json_string_value(json_object_get(message_json, "action")));
        messages[i].message = str_clone(json_string_value(json_object_get(message_json, "message")));
        messages[i].reason = str_clone(json_string_value(json_object_get(message_json, "reason")));
        messages[i].success = json_is_true(json_object_get(message_json, "success"));
    }
    return messages;
}

event_t * json_to_events(json_t * json) {
    event_t * events = (event_t *) malloc(json_array_size(json) * sizeof(event_t));
    int i;
    for (i = 0; i < json_array_size(json); i++) {
        json_t * event_json = json_array_get(json, i);
        events[i].room_id = str_clone(json_string_value(json_object_get(event_json, "room_id")));

        const char * name_s = json_string_value(json_object_get(event_json, "name"));
        if (!strcmp(name_s, "DEPLETEDSNACKTABLE")) {
            events[i].name = DEPLETED_SNACK_TABLE;
        } else if (!strcmp(name_s, "PROFESSOR")) {
            events[i].name = PROFESSOR_ARRIVED;
        } else if (!strcmp(name_s, "NOPROFESSOR")) {
            events[i].name = NO_PROFESSOR;
        } else if (!strcmp(name_s, "PRACTICE")) {
            events[i].name = PRACTICE;
        }
    }
    return events;
}

received_turn_t * json_to_received_turn(json_t * root) {
    received_turn_t * turn = (received_turn_t *) malloc(sizeof(received_turn_t));

    json_t * stats_json = json_object_get(root, "aiStats");
    turn->ai_stats.complexity = json_number_value(json_object_get(stats_json, "complexity"));
    turn->ai_stats.implementation = json_number_value(json_object_get(stats_json, "implementation"));
    turn->ai_stats.optimization = json_number_value(json_object_get(stats_json, "optimization"));
    turn->ai_stats.stability = json_number_value(json_object_get(stats_json, "stability"));
    turn->ai_stats.theory = json_number_value(json_object_get(stats_json, "theory"));

    json_t * errors_json = json_object_get(root, "errors");
    turn->errors = json_to_string_array(errors_json);
    turn->num_errors = json_array_size(errors_json);

    json_t * people_json = json_object_get(root, "people");
    turn->people = json_object_to_people(people_json);
    turn->num_people = json_object_size(people_json);

    json_t * rooms_json = json_object_get(root, "map");
    turn->rooms = json_to_rooms(rooms_json);
    turn->num_rooms = json_object_size(rooms_json);

    json_t * messages_json = json_object_get(root, "messages");
    turn->messages = json_to_messages(messages_json);
    turn->num_messages = json_array_size(messages_json);

    json_t * events_json = json_object_get(root, "events");
    turn->events = json_to_events(events_json);
    turn->num_events = json_array_size(events_json);

    return turn;
}

initial_received_t * json_to_initial_received(json_t * root) {
    initial_received_t * turn = (initial_received_t *) malloc(sizeof(initial_received_t));

    turn->success = !strcmp("Success", json_string_value(json_object_get(root, "status")));

    turn->errors = json_to_string_array(json_object_get(root, "errors"));
    turn->num_errors = json_array_size(json_object_get(root, "errors"));

    if (!turn->success) {
        return turn;
    }

    turn->team_members = json_object_to_people(json_object_get(root, "team"));
    turn->num_team_members = json_object_size(json_object_get(root, "team"));

    turn->team_name = str_clone(json_string_value(json_object_get(root, "team_name")));
    turn->team_id = json_integer_value(json_object_get(root, "team_id"));

    turn->turns_per_hour = json_integer_value(json_object_get(root, "turns_per_hour"));

    return turn;
}

int has_game_ended(json_t * root) {
    return json_object_get(root, "winner") != NULL;
}

json_t * initial_sent_to_json(initial_sent_t * sent_turn) {
    json_t * sent = json_object();
    json_object_set_new_nocheck(sent, "team", json_string(sent_turn->team_name));
    json_t * members = json_array();

    int i;
    for (i = 0; i < sent_turn->num_members; i++) {
        json_t * member = json_object();
        json_object_set_new_nocheck(member, "name", json_string(sent_turn->members[i].name));

        json_t * archetype_json;
        switch (sent_turn->members[i].archetype) {
            case CODER:
                archetype_json = json_string("Coder");
                break;
            case ARCHITECT:
                archetype_json = json_string("Architect");
                break;
            case THEORIST:
                archetype_json = json_string("Theorist");
                break;
            case INFORMANT:
                archetype_json = json_string("Informant");
                break;
        }
        json_object_set_new_nocheck(member, "archetype", archetype_json);

        json_array_append_new(members, member);
    }

    json_object_set_new_nocheck(sent, "members", members);

    return sent;
}

json_t * sent_turn_to_json(sent_turn_t * sent_turn) {
    json_t * actions = json_array();

    int i;
    for (i = 0; i < sent_turn->num_actions; i++) {
        json_t * action = json_object();
        json_t * action_name;
        json_t * action_type;
        switch (sent_turn->actions[i].action) {
            case MOVE:
                json_object_set_new_nocheck(action, "room", json_string(sent_turn->actions[i].room_id));
                action_name = json_string("move");
                break;
            case EAT:
                action_name = json_string("eat");
                break;
            case DISTRACT:
                action_name = json_string("distract");
                json_object_set_new_nocheck(action, "victim", json_integer(sent_turn->actions[i].victim));
                break;
            case SLEEP:
                action_name = json_string("sleep");
                break;
            case CODE:
                switch (sent_turn->actions[i].type) {
                    case IMPLEMENT:
                        action_type = json_string("implement");
                        break;
                    case TEST:
                        action_type = json_string("test");
                        break;
                    case REFACTOR:
                        action_type = json_string("refactor");
                        break;
                    case OPTIMIZE:
                        action_type = json_string("optimize");
                        break;
                }
                json_object_set_new_nocheck(action, "type", action_type);
                action_name = json_string("code");
                break;
            case THEORIZE:
                action_name = json_string("theorize");
                break;
            case VIEW:
                action_name = json_string("view");
                break;
            case WAKE_UP:
                json_object_set_new_nocheck(action, "victim", json_integer(sent_turn->actions[i].victim));
                action_name = json_string("wake");
                break;
            case SPY:
                action_name = json_string("spy");
                break;
        }
        json_object_set_new_nocheck(action, "person_id", json_integer(sent_turn->actions[i].person_id));
        json_object_set_new_nocheck(action, "action", action_name);
        json_array_append_new(actions, action);
    }

    return actions;
}

#endif
