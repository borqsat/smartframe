import datetime
import functools


def duration(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        results = fn(*args, **kwargs)
        duration = datetime.datetime.now() - start
        print "%s took %f secs." % (fn.__name__, duration.total_seconds())
        return results
    return wrapper
