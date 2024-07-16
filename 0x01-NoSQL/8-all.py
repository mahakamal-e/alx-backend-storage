#!/usr/bin/env python3
""" Define function that lists all document"""


def list_all(mongo_collection):
    """Return an empty list if no document in the collection"""
    return mongo_collection.find()
