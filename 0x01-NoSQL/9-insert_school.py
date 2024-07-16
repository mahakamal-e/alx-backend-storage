#!/usr/bin/env python3
""" define insert_school function """


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection based on kwargs"""
    new_items = mongo_collection.insert_one(kwargs)
    return new_items.inserted_id
