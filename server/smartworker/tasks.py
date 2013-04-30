from __future__ import absolute_import

from smartworker.worker import worker as w


@w.task
def add(x, y):
    return x + y


@w.task
def mul(x, y):
    return x * y


@w.task
def xsum(numbers):
    return sum(numbers)
