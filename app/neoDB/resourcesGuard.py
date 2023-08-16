# https://stackoverflow.com/questions/6307761/how-to-decorate-all-functions-of-a-class-without-typing-it-over-and-over-for-eac
# example:
# @for_all_methods(sanitize_args_and_kwargs)
# class userResources:
def for_all_methods(decorator):
    def wrapper(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return wrapper


# the actual sanitize logic's implementation
def sanitize(value):

    return value


def sanitize_args_and_kwargs(function):
    def wrapper(*args, **kwargs):
        for each in args:
            each = sanitize(each)
        for key in kwargs:
            kwargs[key] = sanitize(kwargs[key])
        return function(*args, **kwargs)

    return wrapper


class InvalidRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


import re

special_charactor = "\\*\\+\\-\\[\\]\\(\\)\\\\\\/._'"
regExpRules = {
    "courseCode": "^[a-zA-Z0-9\s]{4,100}$",
    "courseName": "^[a-zA-Z][a-zA-Z0-9\s" + special_charactor + "]{3,99}$",
    "userName": "^[a-zA-Z0-9\s]{4,100}$",
    "userId": "^[-\w\.]+$",
    "email": "^[-\w\.]+@([\w-]+\.)+[\w-]{2,4}$",
    "name": "^[a-zA-Z0-9"
    + special_charactor
    + "][a-zA-Z0-9\s"
    + special_charactor
    + "]{0,99}$",
    "title": "^[a-zA-Z"
    + special_charactor
    + "][a-zA-Z0-9\s"
    + special_charactor
    + "]{3,500}$",
    "tag": "^[-:,a-zA-Z0-9\s.]{4,100}$",
}
regExpRules["desc"] = regExpRules["name"]
regExpRules["ownerId"] = regExpRules["userId"]
regExpRules["h_name"] = regExpRules["name"]
regExpRules["r_name"] = regExpRules["name"]
regExpRules["t_name"] = regExpRules["name"]
regExpRules["w_tag"] = regExpRules["tag"]
# this would force the function to ignore all positional argument
def reject_invalid(function):
    def wrapper(self, *args, **kwargs):
        if (
            "courseCode" in kwargs
            and re.search(regExpRules["courseCode"], kwargs["courseCode"]) == None
        ):
            raise InvalidRequest("Invalid course code pattern")
        if (
            "courseName" in kwargs
            and re.search(regExpRules["courseName"], kwargs["courseName"]) == None
        ):
            raise InvalidRequest("Invalid course name pattern")
        if (
            "userName" in kwargs
            and re.search(regExpRules["userName"], kwargs["userName"]) == None
        ):
            raise InvalidRequest("Invalid user name pattern")
        if (
            "userId" in kwargs
            and kwargs["userId"] is not None
            and re.search(regExpRules["userId"], kwargs["userId"]) == None
        ):
            raise InvalidRequest("Invalid userId pattern.")
        if (
            "ownerId" in kwargs
            and re.search(regExpRules["ownerId"], kwargs["ownerId"]) == None
        ):
            raise InvalidRequest("Invalid ownerId pattern.")
        if "visibility" in kwargs:
            if isinstance(kwargs["visibility"], str):
                try:
                    kwargs["visibility"] = int(kwargs["visibility"])
                except:
                    raise InvalidRequest("Invalid visibility pattern.")
            if kwargs["visibility"] not in [0, 1, 2, 3, 4]:
                raise InvalidRequest("Invalid visibility pattern.")
        if "email" in kwargs and len(kwargs["email"]) >= 320:
            raise InvalidRequest("A valid email should have less then 320 characters")
        if (
            "email" in kwargs
            and re.search(regExpRules["email"], kwargs["email"]) == None
        ):
            raise InvalidRequest("E-mail must be in valid format")
        if "name" in kwargs and re.search(regExpRules["name"], kwargs["name"]) == None:
            raise InvalidRequest("Invalid name pattern.")
        if (
            "h_name" in kwargs
            and re.search(regExpRules["h_name"], kwargs["h_name"]) == None
        ):
            raise InvalidRequest("Invalid head entity name pattern.")
        if (
            "r_name" in kwargs
            and re.search(regExpRules["r_name"], kwargs["r_name"]) == None
        ):
            raise InvalidRequest("Invalid relationship name pattern.")
        if (
            "t_name" in kwargs
            and re.search(regExpRules["t_name"], kwargs["t_name"]) == None
        ):
            raise InvalidRequest("Invalid tail entity name pattern.")
        if (
            "h_name" in kwargs
            and "t_name" in kwargs
            and kwargs["h_name"] == kwargs["t_name"]
        ):
            raise InvalidRequest(
                "Invalid triple pattern, self-referencing is not allowed."
            )
        if "text" in kwargs and (len(kwargs["text"]) < 4 or len(kwargs["text"]) > 500):
            raise InvalidRequest("Invalid text pattern.")
        if "desc" in kwargs and re.search(regExpRules["desc"], kwargs["desc"]) == None:
            raise InvalidRequest("Invalid text pattern.")
        if (
            "title" in kwargs
            and re.search(regExpRules["title"], kwargs["title"]) == None
        ):
            raise InvalidRequest("Invalid text pattern.")
        if "week" in kwargs and not (
            type(kwargs["week"]) == int or type(kwargs["week"]) == float
        ):
            raise InvalidRequest("Invalid week value.")
        if "tag" in kwargs and re.search(regExpRules["tag"], kwargs["tag"]) == None:
            raise InvalidRequest("Invalid tag pattern.")
        if "r_value" in kwargs and not isinstance(kwargs["r_value"], bool):
            raise InvalidRequest("Invalid r_value.")
        if "isInternal" in kwargs and not isinstance(kwargs["isInternal"], bool):
            raise InvalidRequest("Invalid isInternal.")
        if (
            "w_tag" in kwargs
            and re.search(regExpRules["w_tag"], kwargs["w_tag"]) == None
        ):
            raise InvalidRequest("Invalid tag pattern.")
        return function(self, **kwargs)

    return wrapper
