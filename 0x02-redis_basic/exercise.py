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

    def get(self, key: str, fn: Optional[Callable[[bytes], any]] = None) -> Optional[any]:
        """
        Retrieves and type-converts the value of a specific key using fn.

        Args:
            key: The key to retrieve from Redis.
            fn: An optional callable to convert the value.

        Returns:
            The value from Redis, converted using fn if provided, or None if the key does not exist.
        """
        value = self._redis.get(key)  # Retrieve the value from Redis
        if value is None:
            return None  # Return None if the key does not exist
        if fn:
            return fn(value)  # Apply the conversion function
        return value  # Return the raw value if no function is provided

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves and type-converts the value of a specific key to str.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The value from Redis as a string, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves and type-converts the value of a specific key to int.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The value from Redis as an integer, or None if the key does not exist.
        """
        return self.get(key, lambda d: int(d))
