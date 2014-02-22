from config.handle_constants import retrieveConstants
# from unittest import TestCase, main
from action import Action

actionBuffer = {}
actionDispatch = {}


def response(status_code, **kwargs):
    kwargs["status"] = status_code
    return kwargs

_TODO = response(500, message="not yet implemented")
_INVALID = response(404, message="invalid call")


def gatherActions(action, *args, **kwargs):
    action = Action(action, args, kwargs)
    actionBuffer[action.key] = action


def handleAction(action):
    """action handler"""
    if action in actionDispatch:
        return actionDispatch[action](action.args, action.kwargs)
    else:
        return response(404, message="invalid call")


def _movePlayer(*args, **kwargs):
    return _TODO
actionDispatch['movePlayer'] = _movePlayer


def _eatFood(*args, **kwargs):
    return _TODO
actionDispatch['eatFood'] = _eatFood


def _sleep(*args, **kwargs):
    return _TODO
actionDispatch['sleep'] = _sleep


def _code(*args, **kwargs):
    return _TODO
actionDispatch['code'] = _code


def _getMap(*args, **kwargs):
    return _TODO
actionDispatch['getMap'] = _getMap


def _info(*args, **kwargs):
    return _TODO
actionDispatch['info'] = _info


def _serverInfo(*args, **kwargs):
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)
actionDispatch['serverInfo'] = _serverInfo
