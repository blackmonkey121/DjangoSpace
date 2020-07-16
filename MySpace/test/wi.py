#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

cache = {}


def lush():
    print('gengxinle ')
    return 1


class CacheFoo(object):

    def __init__(self, key: str, value: object = None, time: int = 5, flush: bool = True, cache: object = cache, *args, **kwargs):

        self._key: str = key
        self._value: object = value
        self._time: int = time
        self._flush: bool = flush
        self._cache: object = cache
        self._stat = False

    def __enter__(self):
        """ 获取值 """

        value = self._cache.get(self._key)
        if value is not None:
            self.value = value
            self._stat = True
        else:
            self.value = None
        return self

    def get(self):
        return self.value



    def __exit__(self, exc_type, exc_val, exc_tb):
        """ 是否更新缓存 """
        lush()


with CacheFoo('money') as c:
    print(c.get())

