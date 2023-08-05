# django redis cluster client

### 配置
* 第一种, ssl及密码设置在options里
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [{"host": "127.0.0.1", "port": "7000"}],
        "OPTIONS": {
            "CLIENT_CLASS": "hypersRedisCluster.client.RedisClusterClient",
            "IGNORE_EXCEPTIONS": True,
            "PASSWORD": "123456"   # 可选参数
            # "REDIS_CLIENT_KWARGS": {"ssl_cert_reqs": None, "ssl":True}
        },
    }
}
```

* 第二种, 如果有ssl,或密码, 配置在location里
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:7000",
        "OPTIONS": {
            "CLIENT_CLASS": "hypersRedisCluster.client.RedisClusterClient",
            "IGNORE_EXCEPTIONS": True,
            # "REDIS_CLIENT_KWARGS": {"ssl_cert_reqs": None, "ssl":True}
        },
    }
}

"""
LOCATION  For example:  
redis://[[username]:[password]]@localhost:7000
rediss://[[username]:[password]]@localhost:7000
""
```

