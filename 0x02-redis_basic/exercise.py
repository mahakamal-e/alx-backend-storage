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

     def get(self, key: str,
             fn: Optional[Callable[[bytes], any]] = None) -> Optional[any]:
        """
        Retrieve the data from Redis by key and apply,
        the optional conversion function.

        Args:
            key: The key for the data in Redis.
            fn: An optional callable that takes bytes and returns the desired format.

        Returns:
            The retrieved data in the desired format, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data as a string.

        Args:
            key: The key for the data in Redis.

        Returns:
            The retrieved data as a string, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data as an integer.

        Args:
            key: The key for the data in Redis.

        Returns:
            The retrieved data as an integer, or None if the key does not exist.
        """
        return self.get(key, lambda d: int(d))
