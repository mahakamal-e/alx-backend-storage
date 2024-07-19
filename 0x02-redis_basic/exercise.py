#!/usr/bin/env python3
""" Create a Cache class. """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function for the decorated method."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)

        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to record input parameters and output values."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key_inputs = method.__qualname__ + ":inputs"
        key_outputs = method.__qualname__ + ":outputs"

        self._redis.rpush(key_inputs, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(key_outputs, output)

        return output
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls to a particular function."""
    redis_obj = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_obj, redis.Redis):
        return

    method_name = fn.__qualname__
    inputs_name = method_name + ':inputs'
    outputs_name = method_name + ':outputs'

    inputs_list = redis_obj.lrange(inputs_name, 0, -1)
    outputs_list = redis_obj.lrange(outputs_name, 0, -1)

    counts = redis_obj.get(method_name).decode('utf-8')

    print(f"{method_name} was called {counts} times:")

    for input, output in zip(inputs_list, outputs_list):
        print(f"{method_name}(*{input.decode('utf-8')}) -> {output}")


class Cache:
    def __init__(self) -> None:
        """Initialize the Cache instance with a Redis client,
        and flush the database."""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
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
        Retrieves and type-converts the value of a specific key using fn.

        Args:
            key: The key to retrieve from Redis.
            fn: An optional callable to convert the value.

        Returns:
            The value from Redis, converted using fn if provided,
            or None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves and type-converts the value of a specific key to str.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The value from Redis as a string,
            or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves and type-converts the value of a specific key to int.

        Args:
            key: The key to retrieve from Redis.

        Returns:
            The value from Redis as an integer,
            or None if the key does not exist.
        """
        return self.get(key, lambda d: int(d))
