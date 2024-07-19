#!/usr/bin/env python3
"""Defines a function to fetch and cache HTML content from a URL."""

import redis
import requests
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def count_and_cache(method: Callable[[str], str]) -> Callable[[str], str]:
    """
    Decorator to count URL accesses and cache the results.
    
    Args:
        method (Callable[[str], str]): The function to decorate.

    Returns:
        Callable[[str], str]: The decorated function with caching and counting.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that increments access count, caches the result,
        and returns the result from the decorated method.
        
        Args:
            url (str): The URL to fetch the page from.

        Returns:
            str: The HTML content of the URL.
        """
        redis_client.incr(f"count:{url}")

        cached_result = redis_client.get(f"result:{url}")
        if cached_result:
            return cached_result.decode("utf-8")

        result = method(url)
        redis_client.setex(f"result:{url}", 10, result)

        return result

    return wrapper


@count_and_cache
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    
    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
