#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

# Create a Cache instance
cache = Cache()

# Call the store method multiple times
cache.store(b"first")
print(cache.get(cache.store.__qualname__))  # This should print the call count for store after the first call

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))  # This should print the updated call count for store
