#!/usr/bin/env python3
"""
Module for caching HTTP requests with Redis.
"""

from functools import wraps
from typing import Callable
import requests
import redis

redis_client = redis.Redis()


def cache_and_track_requests(fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Decorator to cache and track page requests.

    This decorator increments a counter for each URL access in Redis,
    checks if the URL's HTML content is cached, and if not, fetches the
    content, caches it with an expiration time of 10 seconds, and returns it.

    Args:
        fn (Callable[[str], str]): The function to decorate, which fetches
                                   the page content from a URL.

    Returns:
        Callable[[str], str]: The decorated function that includes caching
                               and access tracking functionality.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Wrapper function that:
        - Increments the access count for the URL in Redis.
        - Checks if the URL's content is cached in Redis.
        - If not cached, fetches the content and caches it with an
          expiration time.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        redis_client.incr(f"count:{url}")

        cached_content = redis_client.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode("utf-8")

        page_content = fn(url)
        redis_client.setex(f"cached:{url}", 10, page_content)

        return page_content

    return wrapper


@cache_and_track_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
