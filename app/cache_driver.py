from flask_caching import Cache
from flask import session, g

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


@cache.memoize()
def user_permission(userId):
    from app.api_driver import get_api_driver

    return get_api_driver().user.get_user_permission(userId=userId)


@cache.memoize()
def user_info(userId):
    from app.api_driver import get_api_driver

    return get_api_driver().user.get_user(userId=userId)


def load_info_from_cache():
    from app.cache_driver import user_permission, user_info

    if "user" in session and "userId" in session["user"]:
        g.permission = user_permission(session["user"]["userId"])
        g.user = user_info(session["user"]["userId"])
    else:
        g.permission = None
        g.user = None