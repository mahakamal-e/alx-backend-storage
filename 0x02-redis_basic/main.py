#!/usr/bin/env python3
"""
Main file to test the Cache class.
"""
from exercise import Cache

def main():
    cache = Cache()

    TEST_CASES = {
        b"foo": None,  # bytes, no conversion
        123: int,      # integer, convert bytes to integer
        "bar": lambda d: d.decode("utf-8")  # string, convert bytes to UTF-8 string
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        result = cache.get(key, fn=fn)
        assert result == value, f"Expected {value} but got {result}"

    # Test get_str and get_int methods
    key_str = cache.store("hello")
    assert cache.get_str(key_str) == "hello"

    key_int = cache.store(456)
    assert cache.get_int(key_int) == 456

    print("All tests passed.")

if __name__ == "__main__":
    main()
