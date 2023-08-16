class UnauthorizedRESTfulRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


from typing import Iterable
from flask import g
from functools import wraps


def authorize_RESTful_with(permissions=[], require_userId=False, roles=[]):
    def authorizer(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            regconized, privileged = permission_check(
                permissions, require_userId, roles
            )
            if not regconized:
                raise UnauthorizedRESTfulRequest("unauthenticated user")
            if not privileged:
                raise UnauthorizedRESTfulRequest("unauthenticated operation")
            return function(*args, **kwargs)

        return wrapper

    return authorizer


class UnauthorizedRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


from typing import Iterable
from flask import session
from functools import wraps


def authorize_with(permissions=[], require_userId=False, roles=[]):
    def authorizer(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            regconized, privileged = permission_check(
                permissions, require_userId, roles
            )
            if not regconized:
                raise UnauthorizedRequest("unauthenticated user")
            if not privileged:
                raise UnauthorizedRequest("unauthenticated operation")
            return function(*args, **kwargs)

        return wrapper

    return authorizer


def permission_check(permissions=[], require_userId=False, roles=[]):
    if require_userId:
        if "user" not in session or "userId" not in session["user"]:
            return False, None
    if (len(permissions) > 0 or len(roles) > 0) and "permission" not in g:
        return False, None
    if len(roles) > 0 and (
        "role" not in g.permission
        or g.permission["role"] is None
        or len(g.permission["role"]) < 1
    ):
        return False, None

    at_least_one_role_fullfiled = len(roles) == 0
    for role in roles:
        if role in g.permission["role"]:
            at_least_one_role_fullfiled = True
    if not at_least_one_role_fullfiled:
        return True, False

    for permission in permissions:
        if isinstance(permission, str):
            if permission not in g.permission or not g.permission[permission]:
                return True, False
        elif isinstance(permission, Iterable):
            at_least_one_permission_fullfiled = False
            for or_permission in permission:
                if or_permission in g.permission and g.permission[or_permission]:
                    at_least_one_permission_fullfiled = True
            if not at_least_one_permission_fullfiled:
                return True, False
    return True, True
