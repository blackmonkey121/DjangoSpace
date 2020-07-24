#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"
from typing import Any

import redis
from django.core.cache import cache
from redis.lock import Lock

# 普通连接
r = redis.Redis(host='localhost', port=6379, db=4)


class RedisLock(Lock):

    def __init__(self, *args, **kwargs):

        super(RedisLock, self).__init__(r, blocking_timeout=0.1, timeout=1, *args, **kwargs)


# def proxy_query(key: str, func: 'function', arg: tuple = None, kw: dict = None, timeout: int = 300) -> Any:
def proxy_query(key: str, func: 'function', timeout: int = 300, *args, **kwargs) -> Any:
    """

    @param key:
    @param func:
    @param arg:
    @param kw:
    @param timeout:
    @return:
    """
    values: Any = cache.get(key)
    if not values:
        with RedisLock('key'):
            values: Any = cache.get(key)
            if not values:
                values: object = func(*args, **kwargs)
                cache.set(key, values, timeout)
    return values