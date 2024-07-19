#!/usr/bin/env python3
"""Test script for get_page function."""

import web

def test_get_page():
    """Test the get_page function with caching and counting."""
    url = "http://slowwly.robertomurray.co.uk"
    
    # Call get_page function multiple times
    content1 = web.get_page(url)
    content2 = web.get_page(url)
    content3 = web.get_page(url)

    # Verify that the function returns the same content
    assert content1 == content2 == content3, "Cache not working correctly"

    # Verify that Redis keys for count and result are set correctly
    assert web.redis_client.get(f"count:{url}"), "URL access count not incremented"
    assert web.redis_client.get(f"result:{url}"), "Result not cached"
    
    # Clean up
    web.redis_client.delete(f"count:{url}")
    web.redis_client.delete(f"result:{url}")

if __name__ == "__main__":
    test_get_page()
    print("All tests passed.")
