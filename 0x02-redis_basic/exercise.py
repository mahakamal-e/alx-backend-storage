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


def replay(fn: Callable):
    '''display the history of calls of a particular function.'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


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
