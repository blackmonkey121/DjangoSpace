#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

REDIS_CACHE_URL = "redis://127.0.0.1:6379/1"
REDIS_SESSION_URL = "redis://127.0.0.1:6379/2"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool'
    },

    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_SESSION_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool'
    }

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# session使用的存储方式
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# 指明使用哪一个库保存session数据
SESSION_CACHE_ALIAS = "session"
