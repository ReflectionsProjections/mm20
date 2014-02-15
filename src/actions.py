from config.handle_constants import retrieveConstants


def response(status_code, **kwargs):
    kwargs["status"] = status_code
    return kwargs

_TODO = response(500, message="not yet implemented")
_INVALID = response(404, message="invalid call")


def handle_action(action, *args, **kwargs):
    """action handler"""
    if action in _action_dispatch:
        return _action_dispatch[action](*args, **kwargs)
    else:
        return response(404, message="invalid call")


def _move_player(*args, **kwargs):
    return _TODO


def _eat_food(*args, **kwargs):
    return _TODO


def _sleep(*args, **kwargs):
    return _TODO


def _code(*args, **kwargs):
    return _TODO


def _get_map(*args, **kwargs):
    return _TODO


def _info(*args, **kwargs):
    return _TODO


def server_info(*args, **kwargs):
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)

_action_dispatch = {"move_player": _move_player, "eat_food": _eat_food,
                    "code": _code, "sleep": _sleep,
                    "server_info": _info, "get_map": _get_map}
