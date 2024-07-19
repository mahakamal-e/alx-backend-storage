#!/usr/bin/env python3
""" Create a Cache class. """
import redis
import uuid
from typing import Union


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
