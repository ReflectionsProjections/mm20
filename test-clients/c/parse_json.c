/*
** Part of the testclient for mechmania 20
**
** The purpose of this file is to parse json into useful data structures.
*/

#include <jansson.h>
#include "ai_objects.c"

received_turn_t * json_to_received_turn(json_t * json) {
    return NULL;
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
