#!/usr/bin/env python3
"""
Defines a function top_students that sorts students by average score.
"""


def top_students(mongo_collection):
    """
    Retrieves all students sorted by average score in descending order.
    """

    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]

    return list(mongo_collection.aggregate(pipeline))
