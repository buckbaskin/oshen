


def cache(func):
    value_call = {}
    def intermediate(*args, **kwargs):
        if (tuple(args), frozenset(kwargs),) not in value_call:
            value_call[(tuple(args), frozenset(kwargs),)] = func(*args, **kwargs)
        return value_call[(tuple(args), frozenset(kwargs),)]
    intermediate.__name__ = func.__name__
    return intermediate
