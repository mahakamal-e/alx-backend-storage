#!/usr/bin/env python3
""" Create a Cache class. """
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self) -> None:
        """Initialize the Cache instance with a Redis client and flush the database."""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a random key and return the key.
        
        Args:
            data: The data to store, which can be a str, bytes, int, or float.
        
        Returns:
            str: The generated random key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

     def get(self, key: str, fn: Union[Callable, None] = None) -> str:
        """Retrieves and type-converts the value of a specific key using fn"""
        value = self._redis.get(key)

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """Retrieves and type-converts the value of a specific key to str."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieves and type-converts the value of a specific key to int."""
        return self.get(key, int)
